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

$packages = [ 'python27', 'python27-distribute', 'python27-devel', 'gcc', 'postgresql-devel' ]
package { $packages:
    ensure      => installed,
    require     => Package['ius-release']
}

user { 'shmir':
    ensure => 'present',
    home   => '/home/shmir',
    shell  => '/bin/bash'
}

exec { 'setup':
    command => 'python2.7 setup.py install',
    cwd     => '/home/shmir/shmir',
    path    => ['/usr/bin', '/usr/sbin', '/bin'],
    user    => 'root',
    require => Package[$packages]
}

#supervisor::service {
#  'shmir':
#    ensure      => present,
#    command     => '/home/vagrant/shmir/bin/uwsgi --xml /home/vagrant/shmir/parts/uwsgi/uwsgi.xml',
#    user        => 'vagrant',
#    group       => 'vagrant',
#}
