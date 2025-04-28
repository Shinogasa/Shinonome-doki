---
title: MEMO：Docker for WindowsでMariaDBが使えない？
date: 2018-06-17 18:02:35
slug: post-512
draft: False
categories:
  - プログラミング
---

こんにちは，しののめ([@Shinogasa](https://twitter.com/Shinogasa))です．

仕事でDocker for Windows上にMySQLを立てていたのですが，都合によりMariaDBに移行することになりました．

そうしたら何か色々エラーが出て使えなかったのでその時の状況をメモ．

docker-compose使っていたので下記のような設定
    
    
    #mysql:
    #    build: ./mysql
    #   volumes:
    #      - ./mysql/data:/var/lib/mysql
    #   ports:
    #      - 3306:3306
    #    environment:
    #      MYSQL_ROOT_PASSWORD: hoge
    #      MYSQL_DATABASE: fuga
    mariadb:
        build: ./mariadb
        volumes:
          - ./mariadb/data:/var/lib/mysql
        ports:
          - 3306:3306
        environment:
          MYSQL_ROOT_PASSWORD: hoge
          MYSQL_DATABASE: fuga

mysqlの設定をそのままmariadbに書き換えただけ．

dockerfileはこう
    
    
    FROM mariadb:latest
    
    EXPOSE 3306
    
    CMD ["mysqld"]

ビルドして立ち上げてみたらこんなエラーが．
    
    
    docker-conpose up mariadb 
    
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] mysqld (mysqld 10.1.22-MariaDB-1~jessie) starting as process 1 ...
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: Using mutexes to ref count buffer pool pages
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: The InnoDB memory heap is disabled
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: GCC builtin __atomic_thread_fence() is used for memory barrier
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: Compressed tables use zlib 1.2.8
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: Using Linux native AIO
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: Using SSE crc32 instructions
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: Initializing buffer pool, size = 256.0M
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] InnoDB: Completed initialization of buffer pool
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [ERROR] InnoDB: auto-extending data file ./ibdata1 is of a different size 0 pages (rounded down to MB) than specified in the .cnf file: initial 768 pages, max 0 (relevant if non-zero) pages!
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [ERROR] InnoDB: Could not open or create the system tablespace. If you tried to add new data files to the system tablespace, and it failed here, you should now edit innodb_data_file_path in my.cnf back to what it was, and remove the new ibdata files InnoDB created in this failed attempt. InnoDB only wrote those files full of zeros, but did not yet use them in any way. But be careful: do not remove old data files which contain your precious data!
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [ERROR] Plugin 'InnoDB' init function returned error.
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [Note] Plugin 'FEEDBACK' is disabled.
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [ERROR] Could not open mysql.plugin table. Some plugins may be not loaded
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [ERROR] Unknown/unsupported storage engine: InnoDB
    mariadb_1  | 2018-06-08  7:59:41 140105323919296 [ERROR] Aborting

/mariadb/data にあるファイル，ディレクトリ(mysql,aria_log.00000001,aria_log.control,ibdta1)を削除して再度起動
    
    
    mariadb_1  | Initializing database
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] /usr/sbin/mysqld (mysqld 10.1.22-MariaDB-1~jessie) starting as process 60 ...
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: Using mutexes to ref count buffer pool pages
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: The InnoDB memory heap is disabled
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: GCC builtin __atomic_thread_fence() is used for memory barrier
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: Compressed tables use zlib 1.2.8
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: Using Linux native AIO
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: Using SSE crc32 instructions
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: Initializing buffer pool, size = 256.0M
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: Completed initialization of buffer pool
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: The first specified data file ./ibdata1 did not exist: a new database to be created!
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [Note] InnoDB: Setting file ./ibdata1 size to 12 MB
    mariadb_1  | 2018-06-08 08:19:53 7efde740b7c0 InnoDB: Error: Write to file ./ibdata1 failed at offset 0.
    mariadb_1  | InnoDB: 1048576 bytes should have been written, only 0 were written.
    mariadb_1  | InnoDB: Operating system error number 22.
    mariadb_1  | InnoDB: Check that your OS and file system support files of this size.
    mariadb_1  | InnoDB: Check also that the disk is not full or a disk quota exceeded.
    mariadb_1  | InnoDB: Error number 22 means 'Invalid argument'.
    mariadb_1  | InnoDB: Some operating system error numbers are described at
    mariadb_1  | InnoDB: http://dev.mysql.com/doc/refman/5.6/en/operating-system-error-codes.html
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [ERROR] InnoDB: Error in creating ./ibdata1: probably out of disk space
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [ERROR] InnoDB: Could not open or create the system tablespace. If you tried to add new data files to the system tablespace, and it failed here, you should now edit innodb_data_file_path in my.cnf back to what it was, and remove the new ibdata files InnoDB created in this failed attempt. InnoDB only wrote those files full of zeros, but did not yet use them in any way. But be careful: do not remove old data files which contain your precious data!
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [ERROR] Plugin 'InnoDB' init function returned error.
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [ERROR] Unknown/unsupported storage engine: InnoDB
    mariadb_1  | 2018-06-08  8:19:53 139628971603904 [ERROR] Aborting
    mariadb_1  |
    mariadb_1  |
    mariadb_1  | Installation of system tables failed!  Examine the logs in
    mariadb_1  | /var/lib/mysql/ for more information.
    mariadb_1  |
    mariadb_1  | The problem could be conflicting information in an external
    mariadb_1  | my.cnf files. You can ignore these by doing:
    mariadb_1  |
    mariadb_1  |     shell> /usr/scripts/scripts/mysql_install_db --defaults-file=~/.my.cnf
    mariadb_1  |
    mariadb_1  | You can also try to start the mysqld daemon with:
    mariadb_1  |
    mariadb_1  |     shell> /usr/sbin/mysqld --skip-grant --general-log &
    mariadb_1  |
    mariadb_1  | and use the command line tool /usr/bin/mysql
    mariadb_1  | to connect to the mysql database and look at the grant tables:
    mariadb_1  |
    mariadb_1  |     shell> /usr/bin/mysql -u root mysql
    mariadb_1  |     mysql> show tables;
    mariadb_1  |
    mariadb_1  | Try 'mysqld --help' if you have problems with paths.  Using
    mariadb_1  | --general-log gives you a log in /var/lib/mysql/ that may be helpful.
    mariadb_1  |
    mariadb_1  | The latest information about mysql_install_db is available at
    mariadb_1  | https://mariadb.com/kb/en/installing-system-tables-mysql_install_db
    mariadb_1  | MariaDB is hosted on launchpad; You can find the latest source and
    mariadb_1  | email lists at http://launchpad.net/maria
    mariadb_1  |
    mariadb_1  | Please check all of the above before submitting a bug report
    mariadb_1  | at http://mariadb.org/jira
    mariadb_1  |
    multi_endpoint_room_management_server_mariadb_1 exited with code 1

なんか再びエラーが．  
色々調べていたらGithubにIssueが立ってました

https://github.com/docker-library/percona/issues/42 

https://github.com/docker-library/mariadb/issues/95 

これ見た感じだとDocker for WindowsではMariaDBが使えないっぽい？

というかMySQL立てた後にそのままMariaDB使うとダメなのかな．

色々試行錯誤してたらvolumesの値を**/var/lib/mysql** から**/var/lib/mariadb** に変えたら問題なく起動してしまいました．
    
    
    mariadb:
        build: ./mariadb
        volumes:
          - ./mariadb/data:/var/lib/mariadb
        ports:
          - 3306:3306
        environment:
          MYSQL_ROOT_PASSWORD: hoge
          MYSQL_DATABASE: fuga

dockerコンテナ上の同じディレクトリを使うとダメなのかもしれないっすね．

でもそのせいで今までMySQLに入れていたデータはMariaDBに引き継ぐことはできませんでした・・・．

やはりCentOS上にDocker立てるのが正解かもしれないですね．

[![](https://images-fe.ssl-images-amazon.com/images/I/51pj9W0WxzL._SL160_.jpg)](https://www.amazon.co.jp/exec/obidos/ASIN/4774170208/deltafantom-22/)

[MariaDB&MySQL全機能バイブル](https://www.amazon.co.jp/exec/obidos/ASIN/4774170208/deltafantom-22/)

posted with [カエレバ](https://kaereba.com)

鈴木 啓修,山田 奈緒子 技術評論社 2014-12-18

[Amazon](https://www.amazon.co.jp/gp/search?keywords=mariadb&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=deltafantom-22)

[楽天市場](//af.moshimo.com/af/c/click?a_id=1052522&p_id=54&pc_id=54&pl_id=616&s_v=b5Rz2P0601xu&url=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2Fmariadb%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0)![](//i.moshimo.com/af/i/impression?a_id=1052522&p_id=54&pc_id=54&pl_id=616)

 

[![](https://images-fe.ssl-images-amazon.com/images/I/51ruD7ljn3L._SL160_.jpg)](https://www.amazon.co.jp/exec/obidos/ASIN/4798153222/deltafantom-22/)

[プログラマのためのDocker教科書 第2版 インフラの基礎知識&コードによる環境構築の自動化](https://www.amazon.co.jp/exec/obidos/ASIN/4798153222/deltafantom-22/)

posted with [カエレバ](https://kaereba.com)

WINGSプロジェクト 阿佐 志保 翔泳社 2018-04-11

[Amazon](https://www.amazon.co.jp/gp/search?keywords=docker&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&tag=deltafantom-22)

[楽天市場](//af.moshimo.com/af/c/click?a_id=1052522&p_id=54&pc_id=54&pl_id=616&s_v=b5Rz2P0601xu&url=https%3A%2F%2Fsearch.rakuten.co.jp%2Fsearch%2Fmall%2Fdocker%2F-%2Ff.1-p.1-s.1-sf.0-st.A-v.2%3Fx%3D0)![](//i.moshimo.com/af/i/impression?a_id=1052522&p_id=54&pc_id=54&pl_id=616)

 
