package { "python2.7-dev":
  ensure => installed,
}

package { "python-virtualenv":
  ensure => installed,
  require => Package['python2.7-dev']
}

package { "libjpeg-dev":
  ensure => installed,
}

package { "zlib1g-dev":
  ensure => installed,
}

package { "libpng12-dev":
  ensure => installed,
}

package { "mysql-server-5.5":
  ensure => installed,
}

package { "libmysqlclient-dev":
  ensure => installed,
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