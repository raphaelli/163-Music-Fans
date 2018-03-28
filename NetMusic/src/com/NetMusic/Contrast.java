package com.NetMusic;

import java.awt.print.Printable;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

public class Contrast {
	ArrayList<String> songuser = new ArrayList<String>();// 创建用户ID列表，方便查询。
	ArrayList<User> usersong = new ArrayList<User>();// 创建用户歌曲信息的存取。
	ArrayList<User> usersong1 = new ArrayList<User>();// 创建用户歌曲信息的存取。
	ArrayList<User> Temporary = new ArrayList<User>();
	Database_Link link;

	Contrast() throws ClassNotFoundException, SQLException {
		link = new Database_Link();
		ResultSet User = link.SqlReturn("show tables");
		while (User.next())
			songuser.add(User.getString(1));
		System.out.println(songuser.get(songuser.size() - 1));
	}
	int inta = 0;

	public int CompareAlgorithm(int a) {
		int sum = 0;
		int c = usersong.size() > usersong1.size() ? usersong1.size() : usersong.size();
		if (a==1) {
			for (int i = 0; i < usersong.size() - 1; i++) {
				for (int j = 0; j < usersong1.size() - 1; j++) {
					String OneSonger = usersong.get(i).Songer;
					String OneSongname = usersong.get(i).SongName;
					String OneSonger1 = usersong1.get(j).Songer;
					String OneSongname1 = usersong1.get(j).SongName;
					if (OneSonger.equals(OneSonger1) && OneSongname.equals(OneSongname1)) {
						sum++;
						System.out.println(OneSonger + ":" + OneSongname);
						System.out.println("2222222222222222222");
					}
				}
			}
			usersong1.clear();
		}
		else if (a==2) 
			
		 {
			for (int i = 0; i < usersong.size() ; i++) {
				for (int j = 0; j < usersong1.size() ; j++) {
					String OneSonger = usersong.get(i).Songer;
					String OneSongname = usersong.get(i).SongName;
					String OneSonger1 = usersong1.get(j).Songer;
					String OneSongname1 = usersong1.get(j).SongName;
					if (OneSonger.equals(OneSonger1) && OneSongname.equals(OneSongname1)) {
						sum++;
						Temporary.add(new User(OneSongname1, OneSonger1,usersong1.get(j).width));
						System.out.println(OneSongname1+":"+OneSonger1);
					}
				}
			}
			if (Temporary.size()>10){
				System.out.println("1111111111111111111111111111111111");
				for (int i = 0; i < Temporary.size() ; i++) {
					System.out.println(Temporary.get(i).SongName+" :"+Temporary.get(i).Songer);
					
				}
				inta++;
				System.out.println("---------------------------------------");
			}
		}
		usersong1.clear();
		Temporary.clear();
		
		
		return sum * 100 / c ;
	}

	public void ComparedMusic(String id1, String id2) {// 对比函数 返回对比信息
		LoadingUser(id1);
		System.out.println("---------------------------------------------");
		LoadingUser1(id2);
		int sum = CompareAlgorithm(1);
		if (sum == 0) {
			System.out.println("匹配值是0！");
		} else {
			int c = usersong.size() > usersong1.size() ? usersong1.size() : usersong.size();
			System.out.println("--------------------------------------------");
			System.out.println("匹配值是" + sum);
		}
	}

	
	public void ComparedMusic(String id) {// 比对整个库
		LoadingUser(id);
		for (int i = 0; i < songuser.size(); i++) {
			String UserId = songuser.get(i).substring(1);
			if (id.equals(UserId)){
				continue;
			}
			System.out.println(i+"-------------------------------------------");
			LoadingUser1(songuser.get(i).substring(1));
			CompareAlgorithm(2);
//			if(i==1){
//				break;
//			}
		}
		System.out.println("有"+inta+"跟你匹配度较高");
	}

	
	public void LoadingUser(String id) {
		ResultSet User;
		try {
			User = link.SqlReturn("select * from a" + id);
			while (User.next()) {
				usersong.add(
						new User(User.getString("songname"), User.getString("songer"), User.getString("percentage")));
			}
		} catch (SQLException e) {
			System.out.print("Id错误~");
		}

	}

	public void LoadingUser1(String id) {
		ResultSet User;
		try {
			User = link.SqlReturn("select * from a" + id);
			while (User.next()) {
				usersong1.add(
						new User(User.getString("songname"), User.getString("songer"), User.getString("percentage")));
			}
		} catch (SQLException e) {
			System.out.print("Id错误~");
		}

	}

}
