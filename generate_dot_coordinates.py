import re
import pandas as pd
import math
import pkg_resources
from configuration import CITY_DISTRIBUTION, SCOPE
from db_operation.db_Initialize import PGInitialize, MYSQLInitialize

MYSQL = MYSQLInitialize()
PG = PGInitialize()

CITY_DISTRIBUTION_FOLDER_PATH = pkg_resources.resource_filename("gauge_point",
                                                                               CITY_DISTRIBUTION)


def gets_the_point_of_the_rectangle(geom_text):
    """
    获取包含城市块的最小矩形的经纬度坐标
    :param geom_text:
    :return:
    """
    geom_text = geom_text.replace("(", "").replace(")", "")
    lon_list = [float(text.split(" ")[0]) for text in geom_text.split(",") if text]
    lat_list = [float(text.split(" ")[-1]) for text in geom_text.split(",") if text]
    return max(lon_list), min(lon_list), max(lat_list), min(lat_list)


def lonlat_to_mercator(lon, lat):
    """
     经纬度坐标转墨卡托坐标
    :param lon:
    :param lat:
    Returns: mercator_x, mercator_y
    """

    mercator_x = lon * 20037508.34 / 180
    mercator_y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    mercator_y = mercator_y * 20037508.34 / 180
    return mercator_x, mercator_y


def mercator_to_lonlat(mercator_x, mercator_y):
    """
    墨卡托坐标转经纬度
    :param mercator_x:
    :param mercator_y:
    :return:  lon, lat
    """
    lon = mercator_x / 20037508.34 * 180
    lat = mercator_y / 20037508.34 * 180
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2);
    return lon, lat


def get_data_mercator(max_lon, min_lon, max_lat, min_lat):
    """
    对矩形区域进行打点
    :param max_lon:
    :param min_lon:
    :param max_lat:
    :param min_lat:
    :return:
    """
    northeast = lonlat_to_mercator(max_lon, max_lat)  # 右上点
    southwest = lonlat_to_mercator(min_lon, min_lat)  # 左下点
    point_list = []
    span = int(int(SCOPE) / math.sqrt(2))
    for x in range(int(southwest[0]), int(northeast[0] + span*2), span*2):
        for y in range(int(southwest[1]), int(northeast[1] + span*2), span*2):
            point_list.append(mercator_to_lonlat(x, y))

    return point_list


def point_save_to_mysql(point_list, city, city_code):
    """

    :param point_list:
    :param city:
    :param city_code:
    :return:
    """
    insert_values = str([(city, city_code, str(point[0]), str(point[1]), 0) for point in point_list])[1:-1]
    sql = f"INSERT INTO  point_coordinates_table (cityName, cityCode, lon, lat, isActivate) VALUES {insert_values}"
    MYSQL.insert(sql)


def get_the_center_point_of_the_circle(city):
    """
    求出打点的经纬度并存入mysql
    :param city:
    :return:
    """
    # 获取城市的边界信息
    city_info = PG.select(
        f"select st_astext(geom), city_code  from country_province_city_boundary WHERE city='{city}'")
    if not city_info:
        raise Exception(f"Unable to access city:{city} geom information")

    city_code = city_info[0][1]
    geom_list = re.findall(r"\(\(.*?\)\)", city_info[0][0])

    for i in geom_list:
        max_lon, min_lon, max_lat, min_lat = gets_the_point_of_the_rectangle(i)
        point_list = get_data_mercator(max_lon, min_lon, max_lat, min_lat)
        point_save_to_mysql(point_list, city, city_code)

    return None


def generate_dot_coordinates_by_cities():
    """
    对城市进行打点
    :return:
    """
    MYSQL.delete("DELETE FROM point_coordinates_table")
    df = pd.read_csv(CITY_DISTRIBUTION_FOLDER_PATH, encoding='utf8')
    df["name"].apply(lambda x: get_the_center_point_of_the_circle(x))


def generate_dot_coordinates_by_nationwide():
    """
    对全国城市进行打点
    :return:
    """
    MYSQL.delete("DELETE FROM point_coordinates_table")
    select_info = PG.select(f"select city from country_province_city_boundary")
    if select_info:
        city_info = [{"name": city[0]} for city in select_info]
        df = pd.DataFrame(city_info)
        df["name"].apply(lambda x: get_the_center_point_of_the_circle(x))
