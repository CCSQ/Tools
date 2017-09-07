# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import time
import subprocess
import os
import os.path
import sys
import time
import shutil
# import pymysql
# import mysql.connector

# 新增颜色，包含到其中
class AddColorCommand(sublime_plugin.TextCommand):
	def run(self, edit, fir='[/0xFF0000]', send='[/0xffffff]'):
		view = self.view
		sels = view.sel() #当前选中
		if len(sels):
			sels = sels[0]
			regionStr = view.substr(sels) #获取选中区域内容
			selContent = fir + regionStr + send
			view.run_command('cut')
			view.insert(edit,sels.begin(),selContent)
			sublime.set_clipboard('')

# 生成sql表头
class SqlTitleCommand(sublime_plugin.TextCommand):
	def run(self, edit, name=''):
		view = self.view
		selContent = '''##############################################################\n#name:''' + time.strftime("%Y%m%d", time.localtime()) + '''[手机魔域][XX脚本]XXX\n#by:''' + name + '''\n#date:''' + time.strftime("%Y-%m-%d", time.localtime()) + '''\n##############################################################\n#注释部分\n\n\n##############################################################\n\n'''
		view.insert(edit,0,selContent)

# 生成lua表头
class LuaTitleCommand(sublime_plugin.TextCommand):
	def run(self, edit, name=''):
		view = self.view
		selContent = '''-- luaId:XXXXX\n--Name:\t\t\t''' + time.strftime("%Y%m%d", time.localtime()) + '''[手机魔域][XX脚本]XXX\n--Creator:\t\t''' + name + '''\n--Created:\t\t''' + time.strftime("%Y-%m-%d", time.localtime()) + '''\n-------------------------------------------------------------------\n\tmodule("Lua_XXXXX",package.seeall)\n-------------------------------------------------------------------\n\n'''
		view.insert(edit,0,selContent)

# 顺延id
class ChangIdCommand(sublime_plugin.TextCommand):
	def run(self, edit, isSequen = 'false'):
		view = self.view
		sels = view.sel() #当前选中
		firstNum = int(view.substr(sels[0]))	#获取第一个数字
		i = 0
		view.run_command('cut')
		if isSequen == 'false':
			for region in self.view.sel():
				view.insert(edit,region.begin(),str(firstNum + i))
				i = i + 1
		else:
			for region in self.view.sel():
				view.insert(edit,region.begin(),str(firstNum - i))
				i = i + 1

# 判断选中字符长度
class GetSelectLenCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sels = view.sel() #当前选中
		if len(sels):
			sels = sels[0]
			regionStr = view.substr(sels)
			leng = len(regionStr)
			utf8_length = len(regionStr.encode('utf-8'))
			print('\n\n当前选中字符串：' + regionStr + '\n\n选中长度：' + str(int((utf8_length-leng)/2 + leng)))
			# sublime.message_dialog('选中长度：' + str(int((utf8_length-leng)/2 + leng)))

# 转换字符串大小写
class SetSelectCharUpperCommand(sublime_plugin.TextCommand):
	def run(self, edit, isupper = True):
		view = self.view
		sels = view.sel() #当前选中
		if len(sels):
			sels = sels[0]
			regionStr = view.substr(sels)
			if isupper:
				regionStr = regionStr.upper()
			else:
				regionStr = regionStr.lower()
			view.run_command('cut')
			view.insert(edit,sels.begin(),regionStr)
			# sublime.message_dialog('选中长度：' + str(int((utf8_length-leng)/2 + leng)))

# 转换驼峰写法
class SetSelectCharHumpCommand(sublime_plugin.TextCommand):
	def run(self, edit, splitStr = "_"):
		view = self.view
		sels = view.sel() #当前选中
		if len(sels):
			sels = sels[0]
			regionStr = view.substr(sels)
			regionStrArr = regionStr.upper().split(splitStr)
			regionStr = ""
			for x in regionStrArr:
				regionStr += x.capitalize()
			regionStr = regionStr[0].lower() + regionStr[1:]
			view.run_command('cut')
			view.insert(edit,sels.begin(),regionStr)
			# sublime.message_dialog('选中长度：' + str(int((utf8_length-leng)/2 + leng)))

# 执行sql
class CommitSqlCommand(sublime_plugin.WindowCommand):
	def run(self, dataName='sjmy31'):
		self.window.run_command('show_panel', {"panel": "console",})
		print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		dir = self.get_path(None)
		dirArr = os.path.splitext(dir)
		end = dirArr[len(dirArr)-1]
		if end != '.sql' and end != '.lua':
			print("刷入文件并非sql或lua")
			return

		print(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
		print('刷入数据库：' + dataName)
		print('刷入文件：' + dir)
		proce = subprocess.Popen( '"python"' + ' "C:\\Users\\Administrator\\AppData\\Roaming\\Sublime Text 3\\Packages\\demo\\sql.py" "' + dataName + '" "' + dir +'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
		returncode = proce.poll()
		while returncode is None:
			line = proce.stdout.readline()
			returncode = proce.poll()
			line = line.strip()
			if line != b'':
				print(line)
		# print(returncode)
		# proce.communicate()
		# print(subprocess.PIPE)

		# conn = pymysql.connect( 
		# 	host="192.168.19.38", 
		# 	# port=3306, 
		# 	user="root", 
		# 	password="aaa", 
		# 	database="sjmy31", 
		# 	autocommit=True, 
		# 	# use_unicode=True, 
		# 	# no_delay=True, 
		# )

		# # conn.select_db('sjmy31')
		# # print(conn)
		# # print(conn.thread_id())
		# # cursor = conn.cursor()
		# # print(cursor.connection.get_host_info())
		# conn.query("use sjmy31")
		# # conn.commit()
		# cursor.close()
		# conn.close()

	# 获取文件位置
	def get_path(self, paths):
		path = None
		if paths:
			path = '*'.join(paths)
		else:
			view = sublime.active_window().active_view()
			path = view.file_name() if view else None
		return path

# 生成MyBatis表头
class MyBatisTitleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view

		firstLine = view.substr(view.line(1))
		if firstLine == '##############':
			print("已有注释，不再生成")
			return

		settings = sublime.load_settings('Tools.sublime-settings')
		MyBatisTitleArr = settings.get("MyBatisTitle")

		selContent = '''##############\n# 多表在不同项目时，需挨个在表前加入表头，配置路径包名，否则取第一张表的设置\n# 包名中的entity等关键字用*号代替\n# 服务端路由默认为after/bean名称\n\n'''
		replaceString = ""
		for x in MyBatisTitleArr.keys():
			replaceString += "#" + MyBatisTitleArr[x] + "\n" + x + "：\n\n"
		selContent += replaceString + '##############\n\n'

		view.insert(edit,0,selContent)

# MyBatis工具
class MyBatisCommand(sublime_plugin.WindowCommand):
	def run(self, createFileName = "all"):
		self.window.run_command('show_panel', {"panel": "console",})
		print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		dir = self.get_path(None)
		if dir:
			dirArr = os.path.splitext(dir)
			end = dirArr[len(dirArr)-1]
			if end != '.sql':
				print("解析文件需为sql")
				return

			print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
			print('解析文件：' + dir)
			self.window.run_command('save')
			self.main_mybatis(dir,createFileName)
		else:
			print("解析的文件并未保存，无法生成数据！")
		
	def main_mybatis(self,dir,createFileName):
		settings = sublime.load_settings('Tools.sublime-settings')
		# sql关键字 -- 忽略
		sqlKey = settings.get("sqlKey")
		author = settings.get("author")

		AllTable = []

		# 单表
		table = {'javaBeanName': { 'beanName':'', 'tableName':'' },'javaBeanVar': []}
		
		# 默认信息
		defaultInfor = {}

		file = open(dir, mode='r', encoding='UTF-8')
		for line in file:
			line = line.expandtabs().lstrip()	# 去掉开头空格
			for key in sqlKey.keys():
				if line.upper().startswith(key) or str(line).upper().startswith(key):
					if not sqlKey[key]:
						# 获取实体名
						if key == 'CREATE TABLE':
							table['javaBeanName'] = self.getJavaBeanName(line)
						# 获取字段
						if key == '`':
							table['javaBeanVar'].append(self.getJavaBeanVar(line))

						# 获取其他信息
						if key == 'PACKAGE':
							temp = self.getOtherInfor(line)
							if temp:
								table['package'] = temp
								# 不存在的话设置数据
								if not 'package' in defaultInfor:
									defaultInfor['package'] = table['package']

						if key == 'PROJECTPATH':
							temp = self.getOtherInfor(line)
							if temp:
								table['projectPath'] = temp
								if not 'projectPath' in defaultInfor:
									defaultInfor['projectPath'] = table['projectPath']

						if key == 'APIPROJECTPATH':
							temp = self.getOtherInfor(line)
							if temp:
								table['apiProjectPath'] = temp
								if not 'apiProjectPath' in defaultInfor:
									defaultInfor['apiProjectPath'] = table['apiProjectPath']

						if key == 'APIPACKAGE':
							temp = self.getOtherInfor(line)
							if temp:
								table['apiPackage'] = temp
								if not 'apiPackage' in defaultInfor:
									defaultInfor['apiPackage'] = table['apiPackage']

						if key == 'SERVICEPROJECTPATH':
							temp = self.getOtherInfor(line)
							if temp:
								table['serviceProjectPath'] = temp
								if not 'serviceProjectPath' in defaultInfor:
									defaultInfor['serviceProjectPath'] = table['serviceProjectPath']

						if key == 'SERVICEPACKAGE':
							temp = self.getOtherInfor(line)
							if temp:
								table['servicePackage'] = temp
								if not 'servicePackage' in defaultInfor:
									defaultInfor['servicePackage'] = table['servicePackage']

						if key == 'MYBATIS':
							if len(line.split('：')) > 1:
								table['myBatis'] = line.split('：')[1].replace('.', '\\').replace('\n', '')
								if not 'myBatis' in defaultInfor:
									defaultInfor['myBatis'] = table['myBatis']

						# 获取表注释
						if key == ') ENGINE=INNODB':
							inforArr = line.split('COMMENT=')
							if len(inforArr) > 1:
								table['comm'] = inforArr[1].replace('\n', '').replace('\'', '').replace(';', '')
							# 下一张表，对tab进行初始化
							if table['javaBeanName']['beanName'] != '':
								AllTable.append(table)
								table = { 'javaBeanName': { 'beanName':'', 'tableName':'' }, 'javaBeanVar': [] }

		defaultInfor['author'] = author

		localPath = dir.split('\\')
		localPath[len(localPath) - 1] = 'Java'
		localPath = "\\".join(localPath)

		self.createAllFile(localPath,AllTable,defaultInfor,createFileName)

		file.close()

	# 获取表名
	def getJavaBeanName(self, line):
		# 忽略的表名关键字
		ignoSqlTableNameKey = sublime.load_settings('Tools.sublime-settings').get('ignoSqlTableNameKey')

		lineArr = line.split('`')
		tableName = lineArr[1]
		nameArr = tableName.split('_')

		name = ""
		for x in nameArr:
			if ignoSqlTableNameKey.count(x) == 0:
				name += x.capitalize()
		return {'beanName': name, 'tableName': tableName}

	# 获取参数
	def getJavaBeanVar(self, line):
		# sql 转java类型 定义
		sqlType = sublime.load_settings('Tools.sublime-settings').get('sqlToJavaType')

		lineArr = line.split('`')
		sqlVar = lineArr[1]

		javaVar = { 'name': '', 'type': '', 'comm': '', 'sqlType': '', 'sqlName': '' }

		sqlvarTemp = sqlVar.split('_')
		if len(sqlvarTemp) > 0:
			javaVar['name'] += sqlvarTemp[0]
		for x in range(1, len(sqlvarTemp)):
			javaVar['name'] += sqlvarTemp[x].capitalize()

		javaBeanTemp = lineArr[2]

		# 获取注释
		COMMENT = javaBeanTemp.split('COMMENT')
		if len(COMMENT) >= 2:
			COMMENT = COMMENT[1].split('\'')
			if len(COMMENT) >= 2:
				javaVar['comm'] = COMMENT[1]

		# 获取sql类型
		for key in sqlType.keys():
			if str(javaBeanTemp).expandtabs().lstrip().lower().startswith(key):
				javaVar['type'] = sqlType[key]
				javaVar['sqlType'] = key
				break
		javaVar['sqlName'] = sqlVar

		return javaVar

	# 获取其余信息
	def getOtherInfor(self, line):
		if len(line.split('：')) > 1:
			return line.split('：')[1].replace(';', '').replace('\n', '')
		return False

	# 生成文件
	def createAllFile(self, path, infor, defaultInfor, createFileName):
		if createFileName == 'all':
			self.clearPath(path)
			os.makedirs(path + '\\bean')
			os.makedirs(path + '\\map')
			os.makedirs(path + '\\dao')
			os.makedirs(path + '\\service')
			os.makedirs(path + '\\service.impl')
			os.makedirs(path + '\\controller')
			os.makedirs(path + '\\html')
			os.makedirs(path + '\\other')

			for x in infor:
				self.createBean(path + '\\bean', x, defaultInfor)
				self.createDao(path + '\\dao',x, defaultInfor)
				self.createMap(path + '\\map',x, defaultInfor)
				self.createService(path + '\\service',x, defaultInfor)
				self.createServiceImpl(path + '\\service.impl',x, defaultInfor)
				self.createController(path + '\\controller',x, defaultInfor)
				self.createOtherInfor(path + '\\other',x, defaultInfor)
				self.createHTML(path + '\\html',x, defaultInfor)
		else:
			if not os.path.exists(path + '\\' + createFileName):
				os.makedirs(path + '\\' + createFileName)

			if createFileName == 'bean':
				for x in infor:
					self.createBean(path + '\\bean', x, defaultInfor)
			if createFileName == 'dao':
				for x in infor:
					self.createDao(path + '\\dao',x, defaultInfor)
			if createFileName == 'map':
				for x in infor:
					self.createMap(path + '\\map',x, defaultInfor)
			if createFileName == 'service':
				if not os.path.exists(path + '\\service.impl'):
					os.makedirs(path + '\\service.impl')
				for x in infor:
					self.createService(path + '\\service',x, defaultInfor)
					self.createServiceImpl(path + '\\service.impl',x, defaultInfor)
			if createFileName == 'controller':
				for x in infor:
					self.createController(path + '\\controller',x, defaultInfor)
			if createFileName == 'other':
				for x in infor:
					self.createOtherInfor(path + '\\other',x, defaultInfor)
			if createFileName == 'html':
				for x in infor:
					self.createHTML(path + '\\html',x, defaultInfor)

	# 清除文件
	def clearPath(self, path):
		if os.path.exists(path):
			current_filelist = os.listdir(path)
			for x in current_filelist:
				real_folder_path  = os.path.join(path,x)
				if os.path.isdir(real_folder_path):
					for root, dirs, files in os.walk(real_folder_path):
						for file in files:
							os.remove(os.path.join(real_folder_path,file))
						for dir in dirs:
							pathTemp = os.path.join(real_folder_path,dir)
							for root, dirs, files in os.walk(pathTemp):
								for file in files:
									os.remove(os.path.join(root,file))
							shutil.rmtree(pathTemp)
					shutil.rmtree(real_folder_path)
			print("非工程路径旧文件清除成功")

	# 获取所需的真实字段
	def getBaseData(self, keyFirst, keySeconnd, object, defaultInfor):
		if keyFirst in object:
			return object[keyFirst]
		elif keySeconnd in object:
			return object[keySeconnd]
		elif keyFirst in defaultInfor:
			return defaultInfor[keyFirst]
		elif keySeconnd in defaultInfor:
			return defaultInfor[keySeconnd]
		else:
			return ""

	# 创建bean
	def createBean(self, path, object, defaultInfor):
		className = object['javaBeanName']['beanName']	# 类名
		beanName = className[0].lower() + className[1:]	# 实体名
		tableName = object['javaBeanName']['tableName']	# 表名
		settings = sublime.load_settings('Tools.sublime-settings')
		comm = ""
		if 'comm' in object:
			comm = " \n\t* 表注释：" + object['comm']

		package = self.getBaseData('apiPackage', 'package', object, defaultInfor)	# 包名
		if package == "":
			package = settings.get('defaultPackageName')
		package = package.replace('*', 'entity', 1)

		pathTemp = self.getBaseData('apiProjectPath', 'projectPath', object, defaultInfor)	# 文件路径
		if pathTemp != "":
			path = pathTemp + '\\src\\main\\java\\' + package.replace('.', '\\')

		author = ""	# 作者
		if 'author' in defaultInfor:
			author = defaultInfor['author']

		# 忽略的字段
		ignoredField = settings.get('ignoredField')

		fp = open(path + '\\' + className + '.java', mode='w', encoding='UTF-8')
		fp.write(
			"package " + package + ";\n\n" + 
			"import java.util.Date;\n" + 
			"import org.apache.ibatis.type.Alias;\n" + 
			"import org.zte.framework.orm.mybatis.entity.DataEntity;\n\n\n" + 
			"\n/**\n\t* 映射表名：" + tableName + comm + " \n\t* 作者：" + author + "\n\t* 时间：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\n*/\n\n" + 
			"@Alias(\"" + beanName + "\")\n" + 
			"public class " + className + " extends DataEntity<Integer> {\n" + 
			"\n\tprivate static final long serialVersionUID = 1L;\n"
		)

		func = ''
		for x in object['javaBeanVar']:
			if x['name'] in ignoredField:
				continue
			String = "\tprivate " + x['type'] + " " + x['name'] + ';'
			if x['comm'] != '':
				String += '\t\t// ' + x['comm']
			fp.write(String + '\n')

			func += '\n\n\tpublic ' + x['type'] + ' get' + x['name'][0].capitalize() + x['name'][1:] + "(){\n\t\treturn " + x['name'] + ";\n\t}"
			func += '\n\n\tpublic void set' + x['name'][0].capitalize() + x['name'][1:] + "(" + x['type'] + ' ' + x['name'] + "){\n\t\tthis." + x['name'] + ' = ' + x['name'] + ";\n\t}"

		fp.write(func + "\n\n}\n")
		fp.close()
		print("生成实体类：" + className)

	# 创建dao
	def createDao(self, path, object, defaultInfor):
		className = object['javaBeanName']['beanName'] + "Dao"
		baseClassName = object['javaBeanName']['beanName']
		settings = sublime.load_settings('Tools.sublime-settings')

		comm = ""
		if 'comm' in object:
			comm = " \n\t* 表注释：" + object['comm']

		author = ""	# 作者
		if 'author' in defaultInfor:
			author = defaultInfor['author']

		apiPackage = self.getBaseData('apiPackage', 'package', object, defaultInfor)	# api包名
		if apiPackage == "":
			apiPackage = settings.get('defaultPackageName')

		package = self.getBaseData('servicePackage', 'package', object, defaultInfor)	# service包名
		if package == "":
			package = settings.get('defaultPackageName')

		pathTemp = self.getBaseData('serviceProjectPath', 'projectPath', object, defaultInfor)	# 文件路径
		if pathTemp != "":
			path = pathTemp + '\\src\\main\\java\\' + package.replace('.', '\\').replace('*', 'dao', 1)

		fp = open(path + '\\' + className + '.java', mode='w', encoding='UTF-8')
		fp.write(
			"package " + package.replace('*', 'dao', 1).replace('\n', '', 1) + ";\n\n" + 
			"import java.util.Map;\n" + 
			"import java.util.List;\n" + 
			"import org.zte.framework.mybatis.paginator.domain.PageBounds;\n" + 
			"import org.zte.framework.mybatis.paginator.domain.PageList;\n" + 
			"import org.zte.framework.orm.mybatis.dao.BaseDao;\n" + 
			"import " + apiPackage.replace('*', 'entity', 1).replace('\n', '', 1) + '.' + baseClassName + ";\n" + 
			"import org.zte.framework.orm.mybatis.MyBatisRepository;\n\n\n" + 
			"\n/**\n\t* 映射表名：" + object['javaBeanName']['tableName'] + comm + " \n\t* 实体：" + baseClassName + " \n\t* 作者：" + author + "\n\t* 时间：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\n*/\n\n" + 
			"@MyBatisRepository\n" + 
			"public interface " + className + " extends BaseDao<" + baseClassName + ",Integer> {" + 

			"\n\t/**\n\t  * 分页查找数据\n\t  * @param map\n\t  * @param pageBounds\n\t  * @return\n\t*/\n" +
			"\tPageList<Map<String, Object>> findByCondition(Map<String, Object> map, PageBounds pageBounds);\n\n" +

			"\n\t/**\n\t  * 不分页查找数据\n\t  * @param map\n\t  * @param pageBounds\n\t  * @return\n\t*/\n" +
			"\tList<Map<String, Object>> findByCondition(Map<String, Object> map);\n\n" +

			"\n\t/**\n\t  * 按条件查找记录数量\n\t  * @param map\n\t  * @return\n\t*/\n" + 
			"\tInteger getCountByCondition(Map<String, Object> map);\n\n" + 

			"}\n"
		)
		fp.close()
		print("生成Dao类：" + className)

	# 创建map
	def createMap(self, path, object, defaultInfor):
		mapName = object['javaBeanName']['beanName'] + "Mapper"
		beanClassName = object['javaBeanName']['beanName']
		tableName = object['javaBeanName']['tableName']
		settings = sublime.load_settings('Tools.sublime-settings')

		comm = ""
		if 'comm' in object:
			comm = "\n\t表注释：" + object['comm']

		author = ""	# 作者
		if 'author' in defaultInfor:
			author = defaultInfor['author']

		apiPackage = self.getBaseData('apiPackage', 'package', object, defaultInfor)	# api包名
		if apiPackage == "":
			apiPackage = settings.get('defaultPackageName')

		package = self.getBaseData('servicePackage', 'package', object, defaultInfor)	# service包名
		if package == "":
			package = settings.get('defaultPackageName')

		pathTemp = self.getBaseData('serviceProjectPath', 'projectPath', object, defaultInfor)	# 文件路径
		if pathTemp != "":
			if 'myBatis' in object:
				path = pathTemp + '\\src\\main\\resources\\mybatis\\' +object['myBatis']
			elif 'myBatis' in defaultInfor:
				path = pathTemp + '\\src\\main\\resources\\mybatis\\' +defaultInfor['myBatis']
			else:
				path = pathTemp + '\\src\\main\\resources\\mybatis'

		fp = open(path + '\\' + mapName + '.xml', mode='w', encoding='UTF-8')
		fp.write(
			'<?xml version="1.0" encoding="UTF-8" ?>\n' + 
			'<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n' + 
			'<!--\n\t描述：表' + object['javaBeanName']['tableName'] + '的SQL映射文件' + comm + 
			'\n\t实体类：' + beanClassName + 
			'\n\t作者：' + author +
			'\n\t时间：' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +' \n-->\n\n' + 
			'<mapper namespace="' + package.replace('*', 'dao', 1).replace('\n', '', 1) + '.' + beanClassName + 'Dao">\n' + 
			'\t<cache type="org.mybatis.caches.ehcache.LoggingEhcache" />\n\n' + 
			'\t<!-- 插入数据 //Generated -->\n' + 
			'\t<insert id="insert">\n' + 
			'\t\tinsert into ' + tableName + '(\n' + 
			'\t\t<if test="id != null">\n' + 
			'\t\t\tid,\n' + 
			'\t\t</if>'
		)
		sqlString = '\n\t\t'
		javaString = '\n\t\t'

		# insert
		javaBeanVar = object['javaBeanVar']
		for x in javaBeanVar:
			if x['sqlName'] == 'id':
				continue
			if x['sqlName'] == javaBeanVar[len(javaBeanVar) - 1]['sqlName']:
				sqlString += x['sqlName']
				javaString += '#{'+ x['name'] +'}'
				break
			sqlString += x['sqlName'] + ',\n\t\t'
			javaString += '#{'+ x['name'] +'},\n\t\t'
		fp.write(
			sqlString + '\n\t\t) values (\n\t\t<if test="id != null">\n\t\t\t#{id},\n\t\t</if>' + javaString + 
			'\n\t\t)\n\t\t<selectKey keyProperty="id" resultType="Integer" order="AFTER"> select LAST_INSERT_ID() </selectKey>\n\t</insert>\n\n\n'
		)

		# delete
		fp.write('\t<!-- 删除数据 //Generated -->\n\t<delete id="delete">\n\t\tdelete from ' + tableName + ' where id = #{id}\n\t</delete>\n\n\n')

		# deletes
		fp.write('\t<!-- 批量删除数据 //Generated -->\n\t<delete id="deletes" parameterType="java.util.List">\n\t\tdelete from ' + tableName + ' where id in\n\t\t<foreach collection="list" index="index" item="item" open="(" separator="," close=")">\n\t\t\t#{item}\n\t\t</foreach>\n\t</delete>\n\n\n')

		# update
		updateString = ''
		for x in javaBeanVar:
			if x['sqlName'] == 'id':
				continue
			if x['sqlName'] == javaBeanVar[len(javaBeanVar) - 1]['sqlName']:
				updateString += 't.' + x['sqlName'] + ' = ' + '#{' + x['name'] + '}'
				break
			updateString += 't.' + x['sqlName'] + ' = ' + '#{' + x['name'] + '},\n\t\t\t'
		fp.write('\t<!-- 更新数据(全字段更新，使用前需先用get设置所有属性) //Generated -->\n\t<update id="update">\n\t\tupdate ' + tableName + ' t\n\t\tset ' +
			updateString + 
			'\n\t\twhere t.id = #{id}\n\t</update>\n\n\n'
		)

		# get
		fp.write('\t<!-- 查询单条数据 //Generated -->\n\t<select id="get" resultType="' + apiPackage.replace('*', 'entity', 1).replace('\n', '', 1) + '.' + beanClassName + '">\n\t\tselect t.id as `id`,' + 
			'\n\t\t\tt.'.join(sqlString.split('\n\t\t')) + 
			'\n\t\tfrom ' + tableName + ' t\n\t\twhere t.id = #{id}\n\t</select>\n\n\n'
		)

		# findByCondition
		getString = ''
		orderBy = ''
		for x in javaBeanVar:
			if x['sqlName'] == 'id':
				continue
			if x['sqlName'] == javaBeanVar[len(javaBeanVar) - 1]['sqlName']:
				getString += 't.' + x['sqlName'] + ' as `' + x['name'] + '`'
				
				break
			getString += 't.' + x['sqlName'] + ' as `' + x['name'] + '`,\n\t\t\t'
		if getString.count('order_num') > 0:
			orderBy = '\n\t\torder by IFNULL(t.order_num,99999)'
		fp.write('\t<!-- 按照条件查询数据 //Generated -->\n\t<select id="findByCondition" resultType="Map">\n\t\tselect t.id as `id`,\n\t\t\t' + 
			getString + '\n\t\tfrom ' + tableName + ' t\n\t\t<where>\n\t\t\t<!-- <if test=""></if> -->\n\t\t\t<!-- <if test="">and </if> -->\n\t\t</where>' + orderBy + '\n\t</select>\n\n\n'
		)

		# getCountByCondition
		fp.write('\t<!-- 按照条件查询数据记录数量 //Generated -->\n\t<select id="getCountByCondition" resultType="Integer">\n\t\tselect count(1) as `cnt`\n\t\tfrom ' + tableName + ' t\n\t\t<where>\n\t\t\t<!-- <if test=""></if> -->\n\t\t\t<!-- <if test="">and </if> -->\n\t\t</where>\n\t</select>')

		fp.write('\n</mapper>')

		fp.close()

		print("生成Map：" + mapName)

	# 创建service
	def createService(self, path, object, defaultInfor):
		className = object['javaBeanName']['beanName'] + "Service"	# 类名
		baseClassName = object['javaBeanName']['beanName']	# bean类名
		package = self.getBaseData('apiPackage', 'package', object, defaultInfor)	# 包名
		settings = sublime.load_settings('Tools.sublime-settings')
		if package == "":
			package = settings.get('defaultPackageName')

		pathTemp = self.getBaseData('apiProjectPath', 'projectPath', object, defaultInfor)	# 文件路径
		if pathTemp != "":
			path = pathTemp + '\\src\\main\\java\\' + package.replace('.', '\\').replace('*', 'service', 1)

		author = ""	# 作者
		if 'author' in defaultInfor:
			author = defaultInfor['author']

		comm = ""
		if 'comm' in object:
			comm = " \n\t* 表注释：" + object['comm']

		fp = open(path + '\\' + className + '.java', mode='w', encoding='UTF-8')
		fp.write(
			"package " + package.replace('*', 'service', 1).replace('\n', '', 1) + ";\n\n" + 
			"import java.util.List;\n" + 
			"import java.util.Map;\n" + 
			"import org.zte.framework.mybatis.paginator.domain.PageBounds;\n" + 
			"import org.zte.framework.page.PageResult;\n" + 
			"import " + package.replace('*', 'entity', 1).replace('\n', '', 1) + '.' + baseClassName + ";\n" + 
			"import org.zte.framework.orm.mybatis.service.BaseService;\n\n\n" + 
			"\n/**\n\t* 映射表名：" + object['javaBeanName']['tableName'] + comm + " \n\t* 实体：" + baseClassName + " \n\t* 作者：" + author + "\n\t* 时间：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\n*/\n\n" + 
			"public interface " + className + " extends BaseService<" + baseClassName + ",Integer> {" + 

			"\n\t/**\n\t  * 分页查找数据\n\t  * @param map\n\t  * @param pageBounds\n\t  * @return\n\t*/\n" +
			"\tpublic PageResult<List<Map<String, Object>>> findByCondition(Map<String, Object> map, PageBounds pageBounds);\n\n" +

			"\n\t/**\n\t  * 不分页查找数据\n\t  * @param map\n\t  * @param pageBounds\n\t  * @return\n\t*/\n" +
			"\tpublic List<Map<String, Object>> findByCondition(Map<String, Object> map);\n\n" +

			"\n\t/**\n\t  * 按条件查找记录数量\n\t  * @param map\n\t  * @return\n\t*/\n" + 
			"\tpublic Integer getCountByCondition(Map<String, Object> map);\n\n" + 

			"}\n"
		)
		fp.close()
		print("生成service类：" + className)

	# 创建createServiceImpl
	def createServiceImpl(self, path, object, defaultInfor):
		className = object['javaBeanName']['beanName'] + "ServiceImpl"
		baseClassName = object['javaBeanName']['beanName']
		settings = sublime.load_settings('Tools.sublime-settings')

		author = ""	# 作者
		if 'author' in defaultInfor:
			author = defaultInfor['author']

		comm = ""
		if 'comm' in object:
			comm = " \n\t* 表注释：" + object['comm']

		package = self.getBaseData('servicePackage', 'package', object, defaultInfor)	# service包名
		if package == "":
			package = settings.get('defaultPackageName')

		pathTemp = self.getBaseData('serviceProjectPath', 'projectPath', object, defaultInfor)	# 文件路径
		if pathTemp != "":
			path = pathTemp + '\\src\\main\\java\\' + package.replace('*', 'service.impl', 1).replace('.', '\\')

		apiPackage = self.getBaseData('apiPackage', 'package', object, defaultInfor)	# api包名
		if apiPackage == "":
			apiPackage = settings.get('defaultPackageName')

		fp = open(path + '\\' + className + '.java', mode='w', encoding='UTF-8')
		fp.write(
			"package " + package.replace('*', 'service.impl', 1).replace('\n', '', 1) + ";\n\n" + 
			"import java.util.List;\n" + 
			"import java.util.Map;\n" + 
			"import org.springframework.stereotype.Service;\n" + 
			"import org.zte.framework.mybatis.paginator.domain.PageBounds;\n" + 
			"import org.zte.framework.orm.mybatis.service.impl.BaseServiceImpl;\n" + 
			"import org.zte.framework.page.PageResult;\n" + 
			"import org.zte.framework.page.PageUtils;\n" + 
			"import " + package.replace('*', 'dao', 1).replace('\n', '', 1) + '.' + baseClassName + "Dao;\n" + 
			"import " + apiPackage.replace('*', 'service', 1).replace('\n', '', 1) + '.' + baseClassName + "Service;\n" + 
			"import " + apiPackage.replace('*', 'entity', 1).replace('\n', '', 1) + '.' + baseClassName + ";\n\n\n" + 
			"\n/**\n\t* 映射表名：" + object['javaBeanName']['tableName'] + comm + " \n\t* 实体：" + baseClassName + " \n\t* 作者：" + author + "\n\t* 时间：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\n*/\n\n" + 
			'@Service("' + baseClassName[0].lower() + baseClassName[1:] + 'Service")\n' + 
			"public class " + className + " extends BaseServiceImpl<" + baseClassName + "Dao," + baseClassName + ",Integer> implements " + baseClassName + "Service {\n\n" + 
			"\t@Override\n\tpublic Integer getCountByCondition(Map<String, Object> map) {\n\t\treturn dao.getCountByCondition(map);\n\t}\n\n" + 
			"\t@Override\n\tpublic PageResult<List<Map<String, Object>>> findByCondition(Map<String, Object> map, PageBounds pageBounds) {\n\t\treturn PageUtils.returnPage(dao.findByCondition(map,pageBounds));\n\t}\n\n" + 
			"\t@Override\n\tpublic List<Map<String, Object>> findByCondition(Map<String, Object> map) {\n\t\treturn dao.findByCondition(map);\n\t}\n\n}"
		)
		fp.close()
		print("生成serviceImpl类：" + className)

	# 创建controller
	def createController(self, path, object, defaultInfor):
		className = object['javaBeanName']['beanName'] + "Controller"
		baseClassName = object['javaBeanName']['beanName']
		serviceBean = baseClassName[0].lower() + baseClassName[1:] + 'Service'
		settings = sublime.load_settings('Tools.sublime-settings')

		comm = ""
		if 'comm' in object:
			comm = "\n\t* 表注释：" + object['comm']

		author = ""	# 作者
		if 'author' in defaultInfor:
			author = defaultInfor['author']

		apiPackage = self.getBaseData('apiPackage', 'package', object, defaultInfor)	# api包名
		if apiPackage == "":
			apiPackage = settings.get('defaultPackageName')

		servicePackage = self.getBaseData('servicePackage', 'package', object, defaultInfor)	# service包名
		if servicePackage == "":
			servicePackage = settings.get('defaultPackageName')

		package = self.getBaseData('package', 'package', object, defaultInfor)	# 包名
		if package == "":
			package = settings.get('defaultPackageName')

		pathTemp = self.getBaseData('projectPath', 'projectPath', object, defaultInfor)	# 文件路径
		if pathTemp != "":
			path = pathTemp + '\\src\\main\\java\\' + package.replace('*', 'controller.after').replace('.', '\\')

		# baseController的位置
		BaseController = "import " + package.split('*')[0] + "BaseController;\n"
		if BaseController.count("main_web") >= 1:
			BaseController = "import com.zte.platform.main_web.web.BaseController;\n"

		fp = open(path + '\\' + className + '.java', mode='w', encoding='UTF-8')
		fp.write(
			"package " + package.replace('*', 'controller.after', 1).replace('\n', '', 1) + ";\n\n" + 
			"import java.util.List;\n" + 
			"import java.util.Map;\n" + 
			"import org.zte.framework.mybatis.paginator.domain.PageBounds;\n" + 
			"import org.zte.framework.result.ResultUtils;\n" + 
			"import org.zte.framework.result.Result;\n" + 
			"import org.zte.framework.bean.MyBeanUtils;\n" + 
			"import javax.servlet.http.HttpServletRequest;\n" + 
			"import javax.servlet.http.HttpServletResponse;\n" + 
			"import org.springframework.stereotype.Controller;\n" + 
			"import org.springframework.beans.factory.annotation.Autowired;\n" + 
			"import org.springframework.web.bind.annotation.ResponseBody;\n" + 
			"import org.springframework.web.bind.annotation.RequestMethod;\n" + 
			"import org.springframework.web.bind.annotation.RequestMapping;\n" + 
			"import org.zte.framework.page.PageResult;\n" + 
			"import com.google.common.collect.Maps;\n" + 
			"import org.springframework.web.bind.annotation.RequestParam;\n\n" + BaseController +
			"import " + servicePackage.replace('*','service') + '.' + baseClassName + "Service;\n" + 
			"import " + apiPackage.replace('*','entity') + '.' + baseClassName + ";\n" + 
			"import " + package.split('*')[0] + "annotation.OperationType;\n" + 
			"import " + package.split('*')[0] + "annotation.SysOperationLog;\n" + 
			"\n/**\n\t* 映射表名：" + object['javaBeanName']['tableName'] + comm + " \n\t* 实体：" + baseClassName + " \n\t* 作者：" + author + "\n\t* 时间：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\n*/\n\n" + 
			"@Controller\n" + 
			'@RequestMapping("after/' + baseClassName[0].lower() + baseClassName[1:] + '")\n' + 
			'public class ' + className + ' extends BaseController {\n' + 
			'\t@Autowired\n\tprivate ' + baseClassName + 'Service ' + serviceBean + ';\n\n' + 
			# data
			'\t/**\n\t* 获取数据列表\n\t* @param request 请求对象\n\t* @param response 响应对象\n\t* @param pageSize 每页条数\n\t* @param currPage 当前页码\n\t* @return\n\t*/\n' + 
			'\t@RequestMapping(value="/data",method=RequestMethod.GET)\n' + 
			'\t@ResponseBody\n' + 
			'\tpublic PageResult<List<Map<String, Object>>> data(\n' + 
			'\t\t\tHttpServletRequest request, HttpServletResponse response,\n' + 
			'\t\t\t@RequestParam(value = "pageSize", defaultValue = "10", required = false) Integer pageSize,\n' + 
			'\t\t\t@RequestParam(value = "currPage", defaultValue = "1", required = false) Integer currPage\n' + 
			'\t){\n' + 
			'\t\t// 参数\n' + 
			'\t\tMap<String, Object> map = Maps.newHashMap();\n\n\n' + 
			'\t\tPageBounds pb = new PageBounds(currPage, pageSize);\n' + 
			'\t\treturn ' + serviceBean + '.findByCondition(map, pb);\n\t}\n\n\n'+

			# get
			'\t/**\n\t* 根据id获取记录数\n\t* @param request 请求对象\n\t* @param response 响应对象\n\t* @param id 根据id获取记录数\n\t* @return\n\t*/\n' + 
			'\t@RequestMapping(value = "/get", method = RequestMethod.GET)\n' + 
			'\t@ResponseBody\n' + 
			'\tpublic Result getData(\n' + 
			'\t\t\tHttpServletRequest request, HttpServletResponse response,\n' + 
			'\t\t\t@RequestParam(value = "id", required = true) Integer id\n' + 
			'\t){\n' + 
			'\t\treturn ResultUtils.returnSuccess("成功", ' + serviceBean + '.get(id));\n\t}\n\n\n' + 

			# deletes
			'\t/**\n\t* 根据ids删除记录数\n\t* @param request 请求对象\n\t* @param response 响应对象\n\t* @param ids 根据ids删除记录数\n\t* @return\n\t*/\n' + 
			'\t@SysOperationLog(description="删除' + baseClassName + '",idField="ids",type=OperationType.delete)\n' + 
			'\t@RequestMapping(value = "/deletes",method = RequestMethod.POST)\n' + 
			'\t@ResponseBody\n' + 
			'\tpublic Result delete(\n' + 
			'\t\t\tHttpServletRequest request, HttpServletResponse response,\n' + 
			'\t\t\t@RequestParam(value="ids",required=true) String ids\n' + 
			'\t){\n' + 
			'\t\treturn ' + serviceBean + '.deletes(ids);\n\t}\n\n\n' + 

			# save
			'\t/**\n\t* 保存记录信息\n\t* @param request 请求对象\n\t* @param response 响应对象\n\t* @param porp 要保存的对象\n\t* @return\n\t*/\n' + 
			'\t@SysOperationLog(description="新增或修改' + baseClassName + '",idField="ids",type=OperationType.saveorupdate)\n' + 
			'\t@RequestMapping(value = "/save",method = RequestMethod.POST)\n' + 
			'\t@ResponseBody\n' + 
			'\tpublic Result save(\n' + 
			'\t\t\tHttpServletRequest request, HttpServletResponse response,\n' + 
			'\t\t\t' + baseClassName + ' porp\n' + 
			'\t){\n' + 

			'\t\tResult result = super.beanValidatorList(porp);\n' + 
			'\t\tif (!result.isSuccess()) return result;\n\n' + 
			'\t\t' + baseClassName + ' saveModel = null;\n' + 
			'\t\tif (porp.getId() == null) {\n' + 
			'\t\t\tsaveModel = new ' + baseClassName + '();\n' + 
			'\t\t} else {\n' + 
			'\t\t\tsaveModel = ' + serviceBean + '.get(porp.getId());\n' + 
			'\t\t}\n\n' + 
			'\t\tMyBeanUtils.propertyUtils(saveModel, porp);\n' + 
			'\t\treturn ' + serviceBean + '.save(saveModel);\n\t}\n\n\n' + 
			
			'}'
		)
		fp.close()
		print("生成controller类：" + className)

	# 创建其余信息
	def createOtherInfor(self, path, object, defaultInfor):
		baseClassName = object['javaBeanName']['beanName']

		settings = sublime.load_settings('Tools.sublime-settings')
		otherTemp = settings.get('otherTemp')

		servicePackage = self.getBaseData('servicePackage', 'package', object, defaultInfor)	# service包名
		if servicePackage == "":
			servicePackage = settings.get('defaultPackageName')

		temp = servicePackage.split('.')
		duboName = temp[len(temp) - 2]

		# dubbo
		serverClass = servicePackage.replace('*','service') + '.' + baseClassName
		serverBean = baseClassName[0].lower() + baseClassName[1:]
		
		fp = open(path + '\\otherInfor.txt', mode='w', encoding='UTF-8')
		fp.write('#生成信息不一定正确\n\n')
		fp.write(otherTemp["dubboService"].replace("server-class", serverClass).replace("server-bean", serverBean))
		fp.write(otherTemp["dubboClient"].replace("server-class", serverClass).replace("server-bean", serverBean))
		fp.close()
		print("生成附加信息")

	# 创建HTML
	def createHTML(self, path, object, defaultInfor):
		baseClassName = object['javaBeanName']['beanName']
		pathName = baseClassName
		htmlListName = baseClassName[0].lower() + baseClassName[1:] + 'List'
		htmlEditName = baseClassName[0].lower() + baseClassName[1:] + 'Edit'
		urlName = baseClassName[0].lower() + baseClassName[1:]
		settings = sublime.load_settings('Tools.sublime-settings')
		htmlTemp = settings.get('htmlTemp')
		jsTemp = settings.get('jsTemp')
		ignoredField = settings.get('ignoredField')

		os.makedirs(path + '\\' + pathName)

		# html - list
		fp = open(path + '\\' + pathName + '\\' + htmlListName + '.html', mode='w', encoding='UTF-8')
		nameTh = ''
		valTd = ''
		for x in object['javaBeanVar']:
			if x['name'] in ignoredField:
				continue
			nameTh += '\t\t\t\t\t\t<th class="text-left-i">' + x['comm'] + '</th>\n'
			valTd += '\t\t\t\t\t\t<td data-title="\'' + x['comm'] + '\'">{{index.' + x['name'] + '}}</td>\n'

		fp.write(htmlTemp['list'].replace('path-name',pathName).replace('html-edit-name',htmlEditName).replace('name-th',nameTh).replace('val-td',valTd))
		fp.close()

		# html - edit
		fp = open(path + '\\' + pathName + '\\' + htmlEditName + '.html', mode='w', encoding='UTF-8')
		editString = ''
		for x in object['javaBeanVar']:
			if x['name'] in ignoredField:
				continue
			if x['name'] in htmlTemp:
				editString += htmlTemp[x['name']].replace('replace-value',x['name']).replace('replace-name',x['comm'])
			elif x['type'] in htmlTemp:
				editString += htmlTemp[x['type']].replace('replace-value',x['name']).replace('replace-name',x['comm'])
			elif x['sqlType'] in htmlTemp:
				editString += htmlTemp[x['sqlType']].replace('replace-value',x['name']).replace('replace-name',x['comm'])
			else:
				editString += htmlTemp['other'].replace('replace-value',x['name']).replace('replace-name',x['comm'])

		fp.write(htmlTemp['edit'].replace('path-name',pathName).replace('edit-string',editString))
		fp.close()

		# js - list
		fp = open(path + '\\' + pathName + '\\' + htmlListName + '.js', mode='w', encoding='UTF-8')
		
		fp.write(jsTemp["list"].replace("path-name",pathName).replace("url-name",urlName).replace("html-edit-name",htmlEditName))

		fp.close()

		# js - edit
		fp = open(path + '\\' + pathName + '\\' + htmlEditName + '.js', mode='w', encoding='UTF-8')
		fp.write(jsTemp["edit"].replace("path-name",pathName).replace("url-name",urlName))
		fp.close()

		print("生成HTML")


	# 获取文件位置
	def get_path(self, paths):
		path = None
		if paths:
			path = '*'.join(paths)
		else:
			view = sublime.active_window().active_view()
			path = view.file_name() if view else None
		return path

	# 显示菜单
	# def is_visible(self):
	# 	view = self.view
	# 	fName = view.file_name()
	# 	vSettings = view.settings()
	# 	syntaxPath = vSettings.get('syntax')
	# 	syntax = ""
	# 	ext = ""

	# 	if (fName != None): # file exists, pull syntax type from extension
	# 		ext = os.path.splitext(fName)[1][1:]
	# 	if(syntaxPath != None):
	# 		syntax = os.path.splitext(syntaxPath)[0].split('/')[-1].lower()

	# 	return ext in ['sql']


class TestCommand(sublime_plugin.WindowCommand):
	def run(self):
		sublime.status_message('Prefixr successfully run on %s selection%s' % (1, '' if 1 == 1 else 's'))