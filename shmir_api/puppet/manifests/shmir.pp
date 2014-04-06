include epel, supervisor

supervisor::service {
  'shmir':
    ensure      => present,
    command     => '/home/vagrant/shmir/bin/uwsgi --xml /home/vagrant/shmir/parts/uwsgi/uwsgi.xml',
    user        => 'vagrant',
    group       => 'vagrant',
}
