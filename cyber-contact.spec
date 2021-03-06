Name:		cyber-contact
# 1.0.<Build>
Version:	%{!?version:1.0.0}%{?version}
# ${commit_count}_${git_commit}
Release:	%{!?release:1}%{?release}
Summary:	Cyberlife Contact API

Group:		Application
License:	GPL
URL:		http://www.cyber-life.cn/
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	python(abi) = 2.7
Requires:	systemd python(abi) = 2.7 nginx

%undefine __check_files

%description

%prep

%build
make

%install
make install DESTDIR=%{buildroot}

%post
/usr/bin/systemctl daemon-reload

/usr/bin/systemctl enable mariadb.service
/usr/bin/systemctl start mariadb.service

count=0
max=3

while ! ls /var/lib/mysql/mysql.sock && [ $count -lt $max ]
do
        sleep 1
        ((++count))
done

mysql -u root 2>&1 < /opt/cyberlife/service/cyber-contact/create_table.sql | tee /root/cyber-contact.rpm.post.log

mkdir -p /opt/cyberlife/logs

systemctl enable cyber-contact.service
systemctl restart cyber-contact.service
systemctl enable cyber-contact-swagger.service
systemctl restart cyber-contact-swagger.service
systemctl enable nginx.service
systemctl restart nginx.service

%postun
/usr/bin/systemctl daemon-reload

%files
/etc/nginx/location.d/*
/etc/nginx/conf.d/*
/opt/cyberlife/service/cyber-contact/*
/etc/systemd/system/*

%doc

%changelog
