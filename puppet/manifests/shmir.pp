include nginx
include supervisor

class { 'postgresql::server':
    postgres_password => 'shmir_dev'
}

package { 'epel-release':
    ensure => installed,
    source => 'http://ftp.pbone.net/pub/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm',
    provider => rpm
}

package { 'ius-release':
    ensure      => installed,
    source      => 'http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-11.ius.centos6.noarch.rpm',
    provider    => rpm,
    require => Package['epel-release']
}

$packages = [
    'python27',
    'python27-distribute',
    'python27-devel',
    'gcc',
    'gcc-c++',
    'erlang',
    'postgresql-devel',
    'vim-minimal',
    'gcc-gfortran',
    'texlive-utils'
]
package { $packages:
    ensure      => installed,
    require     => Package['ius-release']
}

class { '::rabbitmq':
    port              => '5672',
    require           => Package[$packages]
}

class { 'redis': }

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

exec { 'setup':
    command => 'python2.7 setup.py install',
    cwd     => '/home/shmir/shmir',
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

exec { 'add-restart':
  command   => 'echo "alias restart=\'sudo supervisorctl restart all\'" >> .bashrc',
  path    => ['/usr/bin', '/usr/sbin', '/bin'],
  cwd       => '/home/vagrant',
  unless    => 'grep -Fxq "alias restart=\'sudo supervisorctl restart all\'" .bashrc',
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
alias restart='sudo supervisorctl restart all'
alias sctl='sudo supervisorctl'",
    require => Exec['setup']
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
port = 5432",
    require => Exec['setup']
}


nginx::resource::vhost { 'localhost':
    proxy => 'http://127.0.0.1:8080'
}

supervisor::program { 'shmir-celery':
    ensure  => present,
    command => 'celery -A shmir.celery.celery worker',
    user    => 'vagrant',
    group   => 'vagrant',
    require     => [ Exec['setup'], File['/etc/shmir.conf'] ]
}

supervisor::program { 'shmir':
    ensure      => present,
    command     => '/usr/bin/shmir',
    user        => 'vagrant',
    group       => 'vagrant',
    require     => [ Exec['setup'], File['/etc/shmir.conf'] ]
}

supervisor::program { 'shmir-dev':
    ensure  => present,
    command => '/usr/bin/python2.7 /home/shmir/shmir/src/shmir/__init__.py',
    user    => 'vagrant',
    group   => 'vagrant',
    require => [ Exec['setup'], File['/etc/shmir.conf'] ]
}
