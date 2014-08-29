exec { "/usr/bin/apt-get update":
  alias => "update"
}

package { "python2.7-dev":
  ensure => installed,
  require => Exec['update'],
}

package { "python-virtualenv":
  ensure => installed,
  require => [Package['python2.7-dev'], Exec['update']]
}

package { "libjpeg-dev":
  ensure => installed,
  require => Exec['update'],
}

package { "zlib1g-dev":
  ensure => installed,
  require => Exec['update'],
}

package { "libpng12-dev":
  ensure => installed,
  require => Exec['update'],
}

package { "git":
  ensure => installed,
  require => Exec['update'],
}

package { "gettext":
  ensure => installed,
  require => Exec['update'],
}

package { "mysql-server-5.5":
  ensure => installed,
  require => Exec['update'],
}

package { "libmysqlclient-dev":
  ensure => installed,
  require => Exec['update'],
}

package { "node-less":
  ensure => installed,
  require => Exec['update'],
}

# Create virtualenv
exec { "/usr/bin/virtualenv /virtualenv":
  creates => "/virtualenv",
  require => Package["python-virtualenv"],
  alias => "virtualenv"
}

# Install dependencies into virtualenv
exec { "/virtualenv/bin/pip install -r /vagrant/src/requirements.txt":
  require => Exec['virtualenv'],
}