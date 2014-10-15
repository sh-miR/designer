# TODO use this module and check why it has problems with Centos/RHEL 7
# include firewall
include nginx
include supervisor

package { 'epel-release':
    ensure   => installed,
    source   => 'http://ftp.icm.edu.pl/pub/Linux/fedora/linux/epel/7/x86_64/e/epel-release-7-2.noarch.rpm',
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

class { 'python':
    version    => 'system',
    pip        => true,
    dev        => true,
    virtualenv => true,
    gunicorn   => false
}

python::requirements { '/home/shmir/shmir/requirements.txt': }

$packages = [
    'gcc',
    'gcc-c++',
    'postgresql-devel',
    'redis',
    'vim-minimal',
    'gcc-gfortran',
    'texlive-epstopdf',
    'ImageMagick',
    'iptables-services',
    'telnet',
    'perl-Archive-Tar',
    'perl-Digest-MD5',
    'perl-File-Temp'
]

package { $packages:
     ensure      => installed,
     require     => Package['epel-release']
}

package { 'ncbi-blast':
    ensure   => installed,
    source   => 'ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-2.2.29+-1.x86_64.rpm',
    provider => rpm
}

service { 'redis':
    ensure   => running,
    enable   => true,
    provider => systemd,
    require  => Package[$packages]
}

# firewall { '100 allow http and https access':
#     port    => [80, 443, 5555, 8080],
#     proto   => tcp,
#     action  => accept,
#     require => Package[$packages],
#     before  => Exec['persist-firewall']
# }

service { 'firewalld':
    ensure => running,
    provider => systemd
}

exec { 'firewall-conf':
    command => '/usr/bin/firewall-cmd --permanent --zone=public --add-port=80/tcp && /usr/bin/firewall-cmd --permanent --zone=public --add-port=5555/tcp && /usr/bin/firewall-cmd --reload',
    require => Service['firewalld']
}

class { '::rabbitmq':
    port    => '5672',
    require => [ Package['epel-release'], Package[$packages] ]
}

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
alias restart='sudo supervisorctl restart all && celery purge -f && sudo service rabbitmq-server restart && redis-cli FLUSHALL && celery amqp queue.purge design && celery amqp queue.purge score && celery amqp queue.purge subtasks && celery amqp queue.purge blast'
alias sctl='sudo supervisorctl'
export PATH=/home/shmir/shmir/bin:\$PATH"
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
    command   => '/usr/bin/celery -A shmir.async.celery worker -l info -n worker1.%%h -Q design',
    directory => '/home/shmir/shmir/src/',
    user      => 'vagrant',
    group     => 'vagrant',
    require   => [ File['/etc/shmir.conf'], Class['python'] ]
}

supervisor::program { 'shmir-celery-worker2':
    ensure    => present,
    command   => '/usr/bin/celery -A shmir.async.celery worker -l info -n worker2.%%h -Q score',
    directory => '/home/shmir/shmir/src/',
    user      => 'vagrant',
    group     => 'vagrant',
    require   => [ File['/etc/shmir.conf'], Class['python'] ]
}

supervisor::program { 'shmir-celery-worker3':
    ensure    => present,
    command   => '/usr/bin/celery -A shmir.async.celery worker --concurrency=4 -l info -n worker3.%%h -Q subtasks',
    directory => '/home/shmir/shmir/src/',
    user      => 'vagrant',
    group     => 'vagrant',
    require   => [ File['/etc/shmir.conf'], Class['python'] ]
}

supervisor::program { 'shmir-celery-worker4':
    ensure    => present,
    command   => '/usr/bin/celery -A shmir.async.celery worker --concurrency=8 -l info -n worker4.%%h -Q blast',
    directory => '/home/shmir/shmir/src/',
    user      => 'vagrant',
    group     => 'vagrant',
    require   => [ File['/etc/shmir.conf'], Class['python'] ]
}

supervisor::program { 'flower':
    ensure    => present,
    command   => '/usr/bin/celery -A shmir.async.celery flower',
    directory => '/home/shmir/shmir/src/',
    user      => 'vagrant',
    group     => 'vagrant',
    require   => [ File['/etc/shmir.conf'], Class['python'] ]
}

supervisor::program { 'shmir':
    ensure  => present,
    command => '/usr/bin/uwsgi --http :8080 --module shmir --callable app',
    directory => '/home/shmir/shmir/src/',
    user    => 'vagrant',
    group   => 'vagrant',
    require => [ File['/etc/shmir.conf'], Class['python'] ]
}
