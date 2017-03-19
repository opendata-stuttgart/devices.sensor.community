# encoding: utf-8

"""
Copyright (c) 2017, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import pymysql
import re
import datetime
from flask import (current_app)
from . import ExternalDataConstants

class ExternalNodes():
  
  def __init__(self):
    self.connection = pymysql.connect(
      host = current_app.config['EXTERNAL_DATABASE_HOST'],
      user = current_app.config['EXTERNAL_DATABASE_USER'],
      password=current_app.config['EXTERNAL_DATABASE_PASSWORD'],
      db = current_app.config['EXTERNAL_DATABASE_DATABASE'],
      charset = 'utf8',
      cursorclass = pymysql.cursors.DictCursor
    )
  
  def __del__(self):
    self.connection.close()
  
  def transform_email(self):
    with self.connection.cursor() as cursor:
      sql = "SELECT id, description FROM sensors_node"
      cursor.execute(sql)
      
      self.connection.commit()
      nodes = cursor.fetchall()
      for node in nodes:
        if node['description']:
          email = re.search(r'[\w\.-]+@[\w\.-]+', node['description'])
          if email:
            email = email.group(0).lower()
            sql = "UPDATE sensors_node SET email = %s WHERE ID = %s" % (self.connection.escape(email), node['id'])
            cursor.execute(sql)
            self.connection.commit()
        
  
  def email_exists(self, email):
    result = False
    try:
      with self.connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM sensors_node WHERE email = %s"
        cursor.execute(sql, (email.lower()))
        
        self.connection.commit()
        result = cursor.fetchone()
    except pymysql.MySQLError as mysql_error:
      current_app.logger.error("email_exists failed with error %s: %s" % (mysql_error[0], mysql_error[1]))
      return -1
    if result == False or result == None:
      return -1
    return result['count']
  
  def get_nodes_by_email(self, email):
    result = False
    try:
      with self.connection.cursor() as cursor:
        sql = "SELECT * FROM sensors_node LEFT JOIN sensors_sensorlocation ON sensors_node.location_id = sensors_sensorlocation.id WHERE sensors_node.email = %s"
        cursor.execute(sql, (email.lower()))
        
        self.connection.commit()
        result = cursor.fetchall()
    except pymysql.MySQLError as mysql_error:
      current_app.logger.error("get_nodes_by_email failed with error %s: %s" % (mysql_error[0], mysql_error[1]))
      return -1
    if result == False or result == None:
      return -1
    return result
  
  def get_node_by_id(self, id, email):
    result = False
    try:
      with self.connection.cursor() as cursor:
        sql = "SELECT * FROM sensors_node LEFT JOIN sensors_sensorlocation ON sensors_node.location_id = sensors_sensorlocation.id WHERE sensors_node.id = %s AND sensors_node.email = %s"
        cursor.execute(sql, (int(id), email.lower()))
        
        self.connection.commit()
        result = cursor.fetchone()
        if 'latitude' in result:
          result['lat'] = result['latitude']
          del(result['latitude'])
        if 'longitude' in result:
          result['lon'] = result['longitude']
          del(result['longitude'])
    except pymysql.MySQLError as mysql_error:
      current_app.logger.error("get_node_by_id failed with error %s: %s" % (mysql_error[0], mysql_error[1]))
      return -1
    if result == False or result == None:
      return -1
    return result
  
  def get_sensors(self, id, email):
    result = False
    try:
      with self.connection.cursor() as cursor:
        sql = "SELECT sensors_sensor.*  FROM sensors_sensor LEFT JOIN sensors_node ON sensors_sensor.node_id = sensors_node.id WHERE node_id = %s AND sensors_node.email = %s"
        cursor.execute(sql, (int(id), email.lower()))
        
        self.connection.commit()
        result = cursor.fetchall()
    except pymysql.MySQLError as mysql_error:
      current_app.logger.error("get_sensors failed with error %s: %s" % (mysql_error[0], mysql_error[1]))
      return -1
    if result == False:
      return -1
    return result
  
  def update_email(self, id, current_email, new_email):
    result = False
    try:
      with self.connection.cursor() as cursor:
        sql = "UPDATE sensors_node SET email = %s WHERE id = %s AND email = %s"
        cursor.execute(sql, (new_email.lower(), int(id), current_email.lower()))
        self.connection.commit()
    except pymysql.MySQLError as mysql_error:
      current_app.logger.error("update_email failed with error %s: %s" % (mysql_error[0], mysql_error[1]))
      return -1
    return True
  
  def update_node_meta(self,
                       id,
                       email,
                       name=None,
                       description=None,
                       description_internal=None,
                       height=None,
                       traffic_in_area=None,
                       industry_in_area=None,
                       oven_in_area=None,
                       street_name=None,
                       street_number=None,
                       postalcode=None,
                       city=None,
                       country=None,
                       lat=None,
                       lon=None,
                       sensor_position=None):
    result = False
    check = self.get_node_by_id(id, email)
    try:
      with self.connection.cursor() as cursor:
        # check if id + email exists
        if check != -1:
          # check if location is used two times
          sql = "SELECT XXlocation_id, COUNT(*) AS count FROM sensors_node WHERE location_id = %s" % check['location_id']
          cursor.execute(sql)
          self.connection.commit()
          num_location_used = cursor.fetchone()['count']
          
          sql_list = []
          # insert new sensors_node
          if num_location_used > 1:
            sql_list = []
            sql_list.append("created = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            sql_list.append("modified = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            sql_list.append("timestamp = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            sql_list.append("indoor = 0")
            sql = "INSERT INTO sensors_sensorlocation SET %s" % (', '.join(sql_list))
            cursor.execute(sql)
            self.connection.commit()
            sql_list.append("location_id = %s" % (cursor.lastrowid))
          
          # update node
          if name != None:
            sql_list.append("name = %s" % (self.connection.escape(name)))
          if description != None:
            sql_list.append("description = %s" % (self.connection.escape(description)))
          if description_internal != None:
            sql_list.append("description_internal = %s" % (self.connection.escape(description_internal)))
          if height != None:
            sql_list.append("height = %s " % (self.connection.escape(height)))
          if sensor_position != None:
            sql_list.append("sensor_position = %s " % (self.connection.escape(sensor_position)))
          sql_list.append("modified = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
          sql = "UPDATE sensors_node SET %s WHERE id = %s AND email = %s" % (', '.join(sql_list), int(id), self.connection.escape(email.lower()))
          cursor.execute(sql)
          self.connection.commit()
          
          # update location
          sql_list = []
          sql_list.append("indoor = 0")
          if traffic_in_area != None:
            sql_list.append("traffic_in_area = %s" % (self.connection.escape(traffic_in_area)))
          if industry_in_area != None:
            sql_list.append("industry_in_area = %s" % (self.connection.escape(industry_in_area)))
          if oven_in_area != None:
            sql_list.append("oven_in_area = %s" % (self.connection.escape(oven_in_area)))
          if street_name != None:
            sql_list.append("street_name = %s" % (self.connection.escape(street_name)))
          if street_number != None:
            sql_list.append("street_number = %s" % (self.connection.escape(street_number)))
          if postalcode != None:
            sql_list.append("postalcode = %s" % (self.connection.escape(postalcode)))
          if city != None:
            sql_list.append("city = %s" % (self.connection.escape(city)))
          if country != None:
            sql_list.append("country = %s" % (self.connection.escape(country)))
          if lat != None:
            sql_list.append("latitude = %s" % (self.connection.escape(round(float(lat), 11))))
          if lon != None:
            sql_list.append("longitude = %s" % (self.connection.escape(round(float(lon), 11))))
          sql_list.append("modified = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
          sql = "UPDATE sensors_sensorlocation SET %s WHERE id = %s" % (', '.join(sql_list), check['location_id'])
          cursor.execute(sql)
          self.connection.commit()
          
          return True
    except pymysql.MySQLError as mysql_error:
      current_app.logger.error("update_node_meta failed with error %s: %s" % (mysql_error.args[0], mysql_error.args[1]))
      return -1
    return -1
  
  def insert_new_node_with_sensors(self, uid=None, email=None):
    try:
      with self.connection.cursor() as cursor:
        sql_list = []
        sql_list.append("created = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("modified = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("location = ''")
        sql_list.append("timestamp = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("description = ''")
        sql_list.append("indoor = 1")
        sql_list.append("owner_id = %s" % (ExternalDataConstants.OWNER_ID))
        sql_list.append("latitude = %s" % (ExternalDataConstants.DEFAULT_LOCATION_LAT))
        sql_list.append("longitude = %s" % (ExternalDataConstants.DEFAULT_LOCATION_LON))
        sql_list.append("city = ''")
        sql_list.append("industry_in_area = 0")
        sql_list.append("oven_in_area = 0")
        sql_list.append("postalcode = ''")
        sql_list.append("street_name = ''")
        sql_list.append("street_number = ''")
        sql_list.append("traffic_in_area = 0")
        sql_list.append("country = ''")
        sql = "INSERT INTO sensors_sensorlocation SET %s" % (', '.join(sql_list))
        cursor.execute(sql)
        self.connection.commit()
        location_id = cursor.lastrowid
        
        sql_list = []
        sql_list.append("created = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("modified = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("uid = %s" % (self.connection.escape(uid)))
        sql_list.append("description = ''")
        sql_list.append("location_id = %s" % (location_id))
        sql_list.append("owner_id = %s" % (ExternalDataConstants.OWNER_ID))
        sql_list.append("description_internal = ''")
        if email:
          sql_list.append("email = %s" % (self.connection.escape(email)))
        else:
          sql_list.append("email = ''")
        sql_list.append("height = 0")
        sql_list.append("sensor_position = 0")
        sql_list.append("name = ''")
        sql = "INSERT INTO sensors_node SET %s" % (', '.join(sql_list))
        cursor.execute(sql)
        self.connection.commit()
        node_id = cursor.lastrowid
        
        sql_list = []
        sql_list.append("created = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("modified = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("description = ''")
        sql_list.append("sensor_type_id = %s" % (ExternalDataConstants.DEFAULT_SENSOR_TYPE_1))
        sql_list.append("node_id = %s" % (node_id))
        sql_list.append("pin = %s" % (ExternalDataConstants.DEFAULT_SENSOR_PIN_1))
        sql_list.append("public = 0")
        sql = "INSERT INTO sensors_sensor SET %s" % (', '.join(sql_list))
        cursor.execute(sql)
        self.connection.commit()
        
        sql_list = []
        sql_list.append("created = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("modified = '%s'" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        sql_list.append("description = ''")
        sql_list.append("sensor_type_id = %s" % (ExternalDataConstants.DEFAULT_SENSOR_TYPE_2))
        sql_list.append("node_id = %s" % (node_id))
        sql_list.append("pin = %s" % (ExternalDataConstants.DEFAULT_SENSOR_PIN_2))
        sql_list.append("public = 0")
        sql = "INSERT INTO sensors_sensor SET %s" % (', '.join(sql_list))
        cursor.execute(sql)
        self.connection.commit()
        node_id = cursor.lastrowid
        return 1
    except pymysql.MySQLError as mysql_error:
      current_app.logger.error("insert_new_node_with_sensors failed with error %s: %s" % (mysql_error[0], mysql_error[1]))
      return -1
    return -1