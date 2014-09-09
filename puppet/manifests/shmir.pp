include firewall
include nginx
include supervisor

package { 'epel-release':
    ensure   => installed,
    source   => 'http://ftp.icm.edu.pl/pub/Linux/fedora/linux/epel/7/x86_64/e/epel-release-7-1.noarch.rpm',
    provider => rpm
}

package { 'puppet-release':
    ensure   => installed,
    source   => 'https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm',
    provider => rpm
}

class { 'postgresql::server':
    require           => Package['epel-release'],
    postgres_password => 'shmir_dev'
}

# package { 'epel-release':
#     ensure => installed,
#     source => 'http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm',
#     provider => rpm
# }

# package { 'ius-release':
#     ensure      => installed,
#     source      => 'http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-13.ius.centos6.noarch.rpm',
#     provider    => rpm,
#     require => Package['epel-release']
# }

class { 'python':
    version    => 'system',
    pip        => true,
    dev        => true,
    virtualenv => true,
    gunicorn   => false
}

python::requirements { '/home/shmir/shmir/requirements.txt': }

$packages = [
    # 'python27',
    # 'python27-setuptools',
    # 'python27-pip',
    # 'python27-devel',
    'gcc',
    'gcc-c++',
    # 'erlang',
    'postgresql-devel',
    'redis',
    'vim-minimal',
    'gcc-gfortran',
    # 'texlive-utils'
    'texlive-epstopdf',
    'ImageMagick',
    'iptables-services'
]

package { $packages:
     ensure      => installed,
     require     => Package['epel-release']
}

service { 'redis':
    ensure   => running,
    provider => systemd,
    require  => Package[$packages]
}

firewall { '100 allow http and https access':
    port    => [80, 443, 5555, 8080],
    proto   => tcp,
    action  => accept,
    require => Package[$packages]
}

class { '::rabbitmq':
    port    => '5672',
    require => [ Package['epel-release'], Package[$packages] ]
}

# class { 'redis':
#     require => Package['epel-release']
# }

user { 'shmir':
    ensure => 'present',
    home   => '/home/shmir',
    shell  => '/bin/bash'
}

exec { 'mfold-setup':
    command => 'sh /home/shmir/shmir/scripts/mfold.sh',
    path    => ['/usr/bin', '/usr/sbin', '/bin'],
    user    => 'root',

    require => Package[$packages]
}

exec { 'python-packages':
    command => 'easy_install-2.7 ipdb',
    path    => ['/usr/bin', '/usr/sbin', '/bin'],
    user    => 'root',
    require => Package[$packages]
}

exec { 'create-database':
    command => 'psql < shmirdesignercreate.sql',
    cwd     => '/home/shmir/shmir',
    path    => ['/usr/bin', '/usr/sbin', '/bin'],
    user    => 'postgres',
    require => [ Package[$packages], Class['postgresql::server'] ]
}

file { '/home/vagrant/.bashrc':
    mode    => 644,
    owner   => vagrant,
    group   => vagrant,
    content => "# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific aliases and functions
alias restart='sudo supervisorctl restart all && celery purge -f && sudo service rabbitmq-server restart'
alias sctl='sudo supervisorctl'"
}

file { '/etc/shmir.conf':
    mode => 644,
    owner => root,
    group => root,
    content => "[database]
name = shmird
user = postgres
password = shmir_dev
host = 127.0.0.1
port = 5432"
}

nginx::resource::vhost { 'localhost':
    proxy => 'http://127.0.0.1:8080'
}

supervisor::program { 'shmir-celery-worker1':
    ensure    => present,
    command   => '/usr/bin/celery -A shmir.celery.celery worker -l info -n worker1.%%h -Q main',
    directory => '/home/shmir/shmir/src/',
    user      => 'vagrant',
    group     => 'vagrant',
    require   => [ File['/etc/shmir.conf'], Class['python'] ]
}

supervisor::program { 'shmir-celery-worker2':
    ensure    => present,
    command   => '/usr/bin/celery -A shmir.celery.celery worker -l info -n worker2.%%h -Q subtasks',
    directory => '/home/shmir/shmir/src/',
    user      => 'vagrant',
    group     => 'vagrant',
    require   => [ File['/etc/shmir.conf'], Class['python'] ]
}

supervisor::program { 'flower':
    ensure    => present,
    command   => '/usr/bin/celery -A shmir.celery.celery flower',
    directory => '/home/shmir/shmir/src/',
    user      => 'vagrant',
    group     => 'vagrant',
    require   => [ File['/etc/shmir.conf'], Class['python'] ]
}

supervisor::program { 'shmir':
    ensure  => present,
    command => '/usr/bin/python /home/shmir/shmir/src/shmir/__main__.py',
    user    => 'vagrant',
    group   => 'vagrant',
    require => [ File['/etc/shmir.conf'], Class['python'] ]
}
