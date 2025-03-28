---
title: docker runで上げたコンテナに docker-compose upで上げたコンテナをlinkする
date: 2018-08-02 23:27:27
slug: post-566
draft: False
categories:
  - Docker
---

## なんでそんなことしたかったの

  * もともとコンテナをitamaeスクリプトでdocker runして立ち上げていた 
    * オプションが増えてきてコマンドが非常に長くなった
  * 何を書いているのかわかりにくかったのでdocker-compose.ymlにオプションを書いて起動することに



## 現状

すでに上がっているコンテナ 

  * mariadb 
    * mysql互換なので
  * redis 
    * ログ

CONTAINER ID | IMAGE | COMMAND | CREATED | STATUS | PORTS | NAMES  
---|---|---|---|---|---|---  
acb7e507f8e2 | mariadb | "docker-entrypoint.s…" | 8 days ago | Up 8 days | 0.0.0.0:3306->3306/tcp | mariadb_1  
a3240056a0a3 | redis:4.0.8 | "docker-entrypoint.s…" | 8 days ago | Up 8 days | 0.0.0.0:6379->6379/tcp | redis_1  
docker-compose upで上げるコンテナ 

  * javaアプリ 
    * Spring BootでDBにつないでる
    * commandオプションにて起動



## docker runのとき
    
    
    execute "docker build . -t #{NAME}" do
      user 'root'
      cwd ROOM_HOME
    end
    
    execute "sudo docker run -d -p 8080:8080 -e TZ=Asia/Tokyo --name #{NAME} --net team_default --link mariadb_1:mysql --link redis_1:redis -v /var/log/app/:/var/log/app/ -v /home/team/app_build/:/home -it #{NAME} java -jar -Dspring.config.location=\"/home/application.yml\" app.jar" do
      user 'root'
      cwd '/home/team'
    end
    

## docker-compose up

上をdocker-compose upにする 
    
    
    # Docker-compose実行
    execute "sudo docker-compose -f docker-compose.dev.yml build" do
      user 'root'
      cwd ROOM_HOME
    end
    
    execute "sudo docker-compose -f docker-compose.dev.yml up -d" do
      user 'root'
      cwd ROOM_HOME
    end
    

`docker-compose.dev.yml`
    
    
    version: '2.2'
    services:
      app:
        container_name: app
        user: 0:0 #root
        build: .
        image: app
        ports:
          - "8080:8080"
        network_mode: app_default #開発用
        environment:
          - TZ=Asia/Tokyo
        volumes:
          - "/var/log/app/:/var/log/app/"
          - "/home/team/app_build/:/home"
        links:
          - mariadb_1:mysql
          - redis_1:redis
        command: java -jar -Dspring.config.location="/home/application.yml" app.jar
    
    
      # external_links:
        #   - mariadb_1:mysql
        # links:
        #   - "mariadb"
        #   - "mariadb:mysql"
        #   - "redis"
    

## 実行

これで起動したところmariadbにうまくつながらなかった 
    
    
    com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
    
    The last packet sent successfully to the server was 0 milliseconds ago. The driver has not received any packets from the server.
            at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
            at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
            at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
            at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
            at com.mysql.jdbc.Util.handleNewInstance(Util.java:425)
            at com.mysql.jdbc.SQLError.createCommunicationsException(SQLError.java:990)
            at com.mysql.jdbc.MysqlIO.<init>(MysqlIO.java:341)
            at com.mysql.jdbc.ConnectionImpl.coreConnect(ConnectionImpl.java:2186)
            at com.mysql.jdbc.ConnectionImpl.connectOneTryOnly(ConnectionImpl.java:2219)
            at com.mysql.jdbc.ConnectionImpl.createNewIO(ConnectionImpl.java:2014)
            at com.mysql.jdbc.ConnectionImpl.<init>(ConnectionImpl.java:776)
            at com.mysql.jdbc.JDBC4Connection.<init>(JDBC4Connection.java:47)
            at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
            at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
            at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
            at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
            at com.mysql.jdbc.Util.handleNewInstance(Util.java:425)
            at com.mysql.jdbc.ConnectionImpl.getInstance(ConnectionImpl.java:386)
            at com.mysql.jdbc.NonRegisteringDriver.connect(NonRegisteringDriver.java:330)
            at org.apache.tomcat.jdbc.pool.PooledConnection.connectUsingDriver(PooledConnection.java:310)
            at org.apache.tomcat.jdbc.pool.PooledConnection.connect(PooledConnection.java:203)
            at org.apache.tomcat.jdbc.pool.ConnectionPool.createConnection(ConnectionPool.java:735)
            at org.apache.tomcat.jdbc.pool.ConnectionPool.borrowConnection(ConnectionPool.java:667)
            at org.apache.tomcat.jdbc.pool.ConnectionPool.init(ConnectionPool.java:482)
            at org.apache.tomcat.jdbc.pool.ConnectionPool.<init>(ConnectionPool.java:154)
            at org.apache.tomcat.jdbc.pool.DataSourceProxy.pCreatePool(DataSourceProxy.java:118)
            at org.apache.tomcat.jdbc.pool.DataSourceProxy.createPool(DataSourceProxy.java:107)
            at org.apache.tomcat.jdbc.pool.DataSourceProxy.getConnection(DataSourceProxy.java:131)
            at org.springframework.jdbc.datasource.DataSourceTransactionManager.doBegin(DataSourceTransactionManager.java:246)
            ... 21 common frames omitted
    Caused by: java.net.UnknownHostException: mysql: Name or service not known
            at java.net.Inet4AddressImpl.lookupAllHostAddr(Native Method)
            at java.net.InetAddress$2.lookupAllHostAddr(InetAddress.java:928)
            at java.net.InetAddress.getAddressesFromNameService(InetAddress.java:1323)
            at java.net.InetAddress.getAllByName0(InetAddress.java:1276)
            at java.net.InetAddress.getAllByName(InetAddress.java:1192)
            at java.net.InetAddress.getAllByName(InetAddress.java:1126)
            at com.mysql.jdbc.StandardSocketFactory.connect(StandardSocketFactory.java:188)
            at com.mysql.jdbc.MysqlIO.<init>(MysqlIO.java:300)
            ... 43 common frames omitted
    

外部のコンテナにつなぐにはexternal_linksを使うらしい <https://docs.docker.com/compose/compose-file/compose-file-v2/#external_links> そもそもlinksがレガシーなオプションだから使わないほうがいいらしい <https://docs.docker.com/compose/compose-file/compose-file-v2/#links> linksのところを変えた 
    
    
    # links:
    #      - mariadb_1:mysql
    #      - redis_1:redis
    external_links:
         - "mariadb_1:mysql"
         - "redis_1:redis"
    

変わらなかった ドッカーのネットワーク確認 
    
    
    [hoge@appserver ~]$ sudo docker network inspect app_default
    [
        {
            "Name": "app_default",
            "Id": "1d8ba01bca9f48859b06e4799ed5b6dc5b1b2a93bb7ab47c2d7e29b5e8c60389",
            "Created": "2018-07-24T18:44:07.49052281+09:00",
            "Scope": "local",
            "Driver": "bridge",
            "EnableIPv6": false,
            "IPAM": {
                "Driver": "default",
                "Options": null,
                "Config": [
                    {
                        "Subnet": "172.18.0.0/16",
                        "Gateway": "172.18.0.1"
                    }
                ]
            },
            "Internal": false,
            "Attachable": false,
            "Ingress": false,
            "ConfigFrom": {
                "Network": ""
            },
            "ConfigOnly": false,
            "Containers": {
                "a3240056a0a32233efe9464e2b88e63f01bbbf10ca6dfb0d33cf97134ef71b69": {
                    "Name": "redis_1",
                    "EndpointID": "b45d6bab39822687ed2eab70b697952c13680aa29fdbac9d06c827endpointid",
                    "MacAddress": "02:42:ac:12:00:02",
                    "IPv4Address": "172.18.0.2/16",
                    "IPv6Address": ""
                },
                "acb7e507f8e263eea495d53699dcb8f271e621000f2b9c5787d575bd2470317e": {
                    "Name": "mariadb_1",
                    "EndpointID": "398fd645f3165378d4720d596be713038e287d7f27a898060b684cendpointid",
                    "MacAddress": "02:42:ac:12:00:04",
                    "IPv4Address": "172.18.0.4/16",
                    "IPv6Address": ""
                }
            },
            "Options": {},
            "Labels": {}
        }
    ]
    
    

同じネットワークには入ってる hostsに追加してみる <https://docs.docker.com/compose/compose-file/compose-file-v2/#extra_hosts-1>
    
    
    # external_links:
    #      - "mariadb_1:mysql"
    #      - "redis_1:redis"
    extra_hosts:
        - "mysql:172.18.0.4"
        - "redis:172.18.0.2"
    

今度はうまくDBにつながってくれた でもDBのコンテナ再起動してip変わってしまったらyaml書き換える必要がありそう ip直打ちじゃなくしたいですね 参考 <https://mag.osdn.jp/17/03/28/190000/2>

[![](https://images-fe.ssl-images-amazon.com/images/I/5130HDgosML._SL160_.jpg)](//af.moshimo.com/af/c/click?a_id=1052536&p_id=170&pc_id=185&pl_id=4062&s_v=b5Rz2P0601xu&url=https%3A%2F%2Fwww.amazon.co.jp%2Fexec%2Fobidos%2FASIN%2F4798153222%2Fref%3Dnosim)![](//i.moshimo.com/af/i/impression?a_id=1052536&p_id=170&pc_id=185&pl_id=4062)

[プログラマのためのDocker教科書 第2版 インフラの基礎知識&コードによる環境構築の自動化](//af.moshimo.com/af/c/click?a_id=1052536&p_id=170&pc_id=185&pl_id=4062&s_v=b5Rz2P0601xu&url=https%3A%2F%2Fwww.amazon.co.jp%2Fexec%2Fobidos%2FASIN%2F4798153222%2Fref%3Dnosim)![](//i.moshimo.com/af/i/impression?a_id=1052536&p_id=170&pc_id=185&pl_id=4062)

posted with [カエレバ](https://kaereba.com)

WINGSプロジェクト 阿佐 志保 翔泳社 2018-04-11 

[Amazon](//af.moshimo.com/af/c/click?a_id=1052536&p_id=170&pc_id=185&pl_id=4062&s_v=b5Rz2P0601xu&url=https%3A%2F%2Fwww.amazon.co.jp%2Fgp%2Fsearch%3Fkeywords%3Ddocker%26__mk_ja_JP%3D%25E3%2582%25AB%25E3%2582%25BF%25E3%2582%25AB%25E3%2583%258A)![](//i.moshimo.com/af/i/impression?a_id=1052536&p_id=170&pc_id=185&pl_id=4062)

[楽天市場](//af.moshimo.com/af/c/click?a_id=1052522&p_id=54&pc_id=54&pl_id=616&s_v=b5Rz2P0601xu&url=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2Fdocker%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0)![](//i.moshimo.com/af/i/impression?a_id=1052522&p_id=54&pc_id=54&pl_id=616)

[Yahooショッピング](//af.moshimo.com/af/c/click?a_id=1052554&p_id=1225&pc_id=1925&pl_id=18502&s_v=b5Rz2P0601xu&url=http%3A%2F%2Fsearch.shopping.yahoo.co.jp%2Fsearch%3Fp%3Ddocker)![](//i.moshimo.com/af/i/impression?a_id=1052554&p_id=1225&pc_id=1925&pl_id=18502)

[7net](//af.moshimo.com/af/c/click?a_id=1052523&p_id=932&pc_id=1188&pl_id=12456&s_v=b5Rz2P0601xu&url=http%3A%2F%2F7net.omni7.jp%2Fsearch%2F%3Fkeyword%3Ddocker%26searchKeywordFlg%3D1)
