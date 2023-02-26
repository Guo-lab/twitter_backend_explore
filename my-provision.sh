#!/usr/bin/env bash

echo 'Start!'

# if this env not exists,  
# conda create -n twit python=3.6
# conda activate twit

if ! [ -e ./mysql-apt-config_0.8.15-1_all.deb ]; then
	wget -c https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb
fi

# sudo xcodebuild -license
#X sudo port -f install dpkg

if [ ! -f "/usr/bin/pip3" ]; then
  echo "need pip3"
else
  echo "pip3 已安装"
fi


#@ https://cdn.mysql.com/archives/mysql-8.0/mysql-8.0.12-macos10.13-x86_64.dmg
sudo vim ~/.bash_profile
# add '''export PATH="/usr/local/mysql/bin:$PATH" ''' into files
source ~/.bash_profile


#X pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# Use conda env 
ln -s /usr/local/mysql/bin/mysql_config /Applications/anaconda3/envs/twit/bin/mysql_config

# 设置mysql的root账户的密码为 yourpassword 安装时已设置
# 创建名为twitter的数据库
sudo mysql -u root -p << 12345678
	# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '12345678';
  flush privileges;
	show databases;
	CREATE DATABASE IF NOT EXISTS twitter;

12345678

echo 'All Done!'