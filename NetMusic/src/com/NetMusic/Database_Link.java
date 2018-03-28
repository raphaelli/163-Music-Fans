package com.NetMusic;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Collection;
import com.mysql.jdbc.Statement;
/*
 * mysql 查询语句
 * 查询所有表：show tables;
 * 查询某一个表：select * from 表名 where 条件;
 * 
 * 
 */
public class Database_Link {

	public Database_Link() throws ClassNotFoundException, SQLException{
		Class.forName("com.mysql.jdbc.Driver");
	}
	String url = "jdbc:mysql://xxx.xxx.xxx.xxx:3306/NeteaseMusicResult?user=xxx&password=xxx";
	Connection conn = DriverManager.getConnection(url);
	
	public ResultSet SqlReturn(String sql) throws SQLException {
		Statement stst = (Statement) conn.createStatement();
		ResultSet resultSetes = stst.executeQuery(sql);
		int sum=0;
		return resultSetes;
		
	}
	public void close() throws SQLException {
		conn.close();
	}
	

		

	}