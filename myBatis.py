#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os

fileName = sys.argv[1]
type = sys.getfilesystemencoding()
print(fileName)


end = os.path.splitext(fileName)
end = end[len(end)-1]

if end != '.sql':
	print("解析文件非sql，解析失败")
	sys.exit()


# sql关键字 -- 忽略
sqlTemp = {
	'#': True,
	'CREATE TABLE': False,	# 生成表
	'`':False,	# 获取字段
}

# sql 转java类型 定义
sqlType = {
	'int': 'Integer',
	'tinyint': 'Boolen',
	'varchar': 'String',
	'text': 'String',
	'timestamp': 'Date'

}

# 忽略的表名关键字
sqlTableName = ['t','sp']

table = []

javaBeanName = {
	'beanName':'',
	'tableName':'',
}
javaBeanVar = []

# 获取表名
def createJavaBeanName(line):
	lineArr = line.split('`')
	tableName = lineArr[1]
	nameArr = tableName.split('_')

	name = ""
	for x in nameArr:
		if sqlTableName.count(x) == 0:
			name += x.capitalize()
	return {'beanName': name, 'tableName': tableName}

def createJavaBeanVar(line):
	lineArr = line.split('`')
	sqlVar = lineArr[1]

	javaVar = {
		'name': '',
		'type': '',
	}
	sqlvarTemp = sqlVar.split('_')
	if len(sqlvarTemp) > 0:
		javaVar['name'] += sqlvarTemp[0]
	for x in range(1, len(sqlvarTemp)):
		javaVar['name'] += sqlvarTemp[x].capitalize()

	javaBeanTemp = lineArr[2]
	print(javaBeanTemp.split('COMMENT')[1].split('\'')[1])
	for key in sqlType.keys():
		if str(javaBeanTemp).expandtabs().lstrip().lower().startswith(key):
			javaVar['type'] = sqlType[key]
			break

	return { 'javaVar':javaVar, 'sqlVar':sqlVar }


file = open(fileName, 'rb')
for line in file:
	line = line.expandtabs().lstrip()	# 去掉开头空格
	for key in sqlTemp.keys():
		if str(line).upper().startswith('B\''+key) or str(line).upper().startswith('B"'+key):
			if not sqlTemp[key]:
				# 获取实体名
				if key == 'CREATE TABLE':
					if javaBeanName['beanName'] != '':
						table.append({'javaBeanName':javaBeanName, 'javaBeanVar':javaBeanVar})
						javaBeanName = { 'beanName':'', 'tableName':'', }
						javaBeanVar = []
					javaBeanName = createJavaBeanName(str(line))
					print("create bean name as : " + javaBeanName['beanName'])
				# 获取字段
				if key == '`':
					javaBeanVar.append(createJavaBeanVar(str(line)))
table.append({'javaBeanName':javaBeanName, 'javaBeanVar':javaBeanVar})



print(table)
# 	if sqlTemp[line.lower()] == false:
# 		print(line)
	
# 		if line.lower().startswith('#delete from'):
# 			sqlList.append(line[1:])
# 		elif line.lower().startswith('delete from'):
# 			sqlList.append(line)
# 		elif line.lower().startswith('insert into'):
# 			sqlList.append(line)
# 		elif line.lower().startswith('update'):
# 			sqlList.append(line)
# 		elif line.startswith('('):
# 			sqlList.append(line)
# 	tempSql = ''.join(sqlList).replace(';\n', ';')
# 	tempList = tempSql.split(';')

# 	tempList.pop()

# 	for sql in tempList:
# 		# print(sql + ';')
# 		try:
# 			cursor.execute(sql + ';')
# 			db.commit()
# 			flag = 1
# 			# print('commit true')
# 		except MySQLdb.Error as e:
# 			flag = 2
# 			print(sql + ';')
# 			print(e[1])
# 			db.rollback()
# 			break

# elif end == '.lua':
# 	file = open(fileName, 'r')
# 	# luaId = file.readline().replace('\n', '')
# 	# luaId = luaId[9:]
# 	luaId = ''
# 	for line in file:
# 		line = line.expandtabs().lstrip()	# 去掉开头空格
# 		if line.lower().startswith('module("'):
# 			fomart = '0123456789'
# 			temp = line.lower().split(',')[0]
# 			for c in line.lower().split(',')[0]:
# 				if not c in fomart:
# 					temp = temp.replace(c,'')
# 			luaId = temp
# 			break

# 	name = file.name
# 	name = name.split('\\')

# 	if luaId == '':
# 		if luaIdDic.has_key(name[len(name)-1]):
# 			luaId = luaIdDic[name[len(name)-1]]
# 		else:
# 			print('module err')
# 			sys.exit()


# 	print('luaId:'+luaId)


# 	nameString = []
# 	for lin in name:
# 		if lin.lower() == 'mywork' or lin.lower() == 'recvmessage' or lin.lower() == 'framework' or lin.lower() == '[手机魔域]lua查错.lua' or len(nameString) > 0:
# 			nameString.append(lin)
# 	nameString = '\\\\'.join(nameString)
# 	index = 0

# 	file.seek(0, 0)
# 	sqlList.append('insert into cq_lua(id,block_id,block_line,block_name,text) values')
# 	selectSql = 'select block_name,text from cq_lua where block_id = ' + str(luaId) + ' order by block_line;'
# 	luaFlag = False
# 	try:
# 		cursor.execute(selectSql)
# 		results = cursor.fetchall()

# 		if len(results) == 0:
# 			print('new script')

# 		num_lines = sum(1 for line in open(fileName))

# 		for line in file:

# 			if len(results) != num_lines:
# 				luaFlag = True
# 			else:
# 				if results[index][0].replace('\\', '\\\\') != nameString or results[index][1].rstrip() != line.rstrip():
# 					# print(results[index][1].rstrip() , line.rstrip())
# 					luaFlag = True

# 			line = line.replace('\\', '\\\\')
# 			line = line.replace('\'', '\\\'')
# 			line = line +'\'),'
# 			line = line.replace('\n\'),', '\'),')
# 			# line = line.replace('\\n', '\\\\n')
# 			tempStr = '(0,' + str(luaId) + ',' + str(index) + ',\''+ nameString +'\',\''+ line
# 			sqlList.append(tempStr)
# 			index += 1

# 	except:
# 		print(selectSql)
# 		print("Error: unable to fecth data")
# 		sys.exit()
# 	if not luaFlag:
# 		print("no change")
# 		sys.exit()

# 	sqlTemp = ''.join(sqlList)
# 	sqlTemp = sqlTemp[0:len(sqlTemp) - 1] + ';'
# 	# print(sqlTemp)

# 	cursor.execute('delete from cq_Load_lua_order where block_id = ' + luaId + ' and sort = ' + luaId + ';')
# 	cursor.execute('delete from cq_lua where block_id = ' + luaId + ';')
# 	cursor.execute('insert into cq_Load_lua_order (id,block_id,sort) values (0,' + luaId + ',' + luaId + ');')
# 	try:
# 		cursor.execute(sqlTemp)
# 		db.commit()
# 		flag = 3
# 	except:
# 		flag = 4


# if flag == 0:
# 	print('mysql err')
# elif flag == 1:
# 	print('commit SQL success')
# elif flag == 2:
# 	print('commit SQL false')
# elif flag == 3:
# 	print('commit Lua success')
# elif flag == 4:
# 	print('commit Lua false')

# cursor.close()
# db.close()

