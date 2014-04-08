include epel, supervisor

supervisor::service {
  'shmir':
    ensure      => present,
    command     => '/home/vagrant/shmir/bin/uwsgi --xml /home/vagrant/shmir/parts/uwsgi/uwsgi.xml',
    user        => 'vagrant',
    group       => 'vagrant',
}

package {
  'ius-release':
    ensure      => installed,
    source      => "http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-11.ius.centos6.noarch.rpm",
    provider    => rpm
}

$packages = [ "python27", "python27-devel" ]
package {
  $packages:
    ensure      => installed,
    require     => Package["ius-release"]
}
