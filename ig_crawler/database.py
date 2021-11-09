import sqlite3
import time

# import ig_crawler.postClass


def main_getinfo(result, db_name, _Table_name):
    """
    get post info
    :param result:
    :param db_name:
    :param _Table_name:
    :return:
    """
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    SQL = '''INSERT INTO '{Table_name}' (username,id,url,typename,edge_media_to_caption,shortcode,taken_at_timestamp ,edge_media_preview_like) VALUES ( "{username}", "{id}" ,"{url}","{typename}" ,"{edge_media_to_caption}", "{shortcode}" , "{taken_at_timestamp}" ,"{edge_media_preview_like}" )'''
    for i in range(len(result)):
        _username = result[i].username
        _id = result[i].id
        # _fbid = result[i].fbid
        _url = result[i].url
        _typename = result[i].typename
        _edge_media_to_caption = result[i].edge_media_to_caption
        B = str(_edge_media_to_caption)
        _shortcode = result[i].shortcode
        _taken_at_timestamp = result[i].taken_at_timestamp
        _edge_media_preview_like = result[i].edge_media_preview_like
        # _owner_id = result[i].owner_id
        # _owner_username = result[i].owner_username

        SQL2 = SQL.format(Table_name=_Table_name, username=_username, id=_id, url=_url, typename=_typename,
                          edge_media_to_caption=B.replace("\"", "\'"), shortcode=_shortcode,
                          taken_at_timestamp=_taken_at_timestamp, edge_media_preview_like=_edge_media_preview_like)
        # print(i)
        # print(SQL2)
        cursor.execute(SQL2)
    # 去掉重複
    sql_query = "DELETE FROM '{Table_name}' WHERE rowid NOT IN(SELECT MAX(rowid) rowid FROM '{Table_name}' GROUP BY shortcode) "
    sql_query = sql_query.format(Table_name=_Table_name)
    cursor.execute(sql_query)
    # 提交
    con.commit()
    cursor.close()
    con.close()
    print("save db over...")


def createTable(db_name, _Table_name):
    SQLcreateQ = \
        """
        CREATE    TABLE    "{Table_name}"(
            "username"    TEXT    COLLATE    NOCASE,
            "id"    TEXT,    "url"    TEXT,
            "typename"    TEXT,
            "edge_media_to_caption"    TEXT,
            "shortcode"    TEXT,
            "taken_at_timestamp"    INTEGER,
            "edge_media_preview_like"    TEXT,
            "is_download"    TEXT    DEFAULT    'False'
        );
        """
    SQLcreateQ = SQLcreateQ.format(Table_name=_Table_name)
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute(SQLcreateQ)
    con.commit()
    cursor.close()
    con.close()


def check(db_name, _Table_name):
    SqlTableQ = "select name from sqlite_master where name = '{Table_name}'"
    SqlTableQ = SqlTableQ.format(Table_name=_Table_name)
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    result = cursor.execute(SqlTableQ).fetchall()
    if (len(result) < 1):
        createTable(db_name, _Table_name)


# def closeDB():
#     con.close()


def main_getindex(result, db_name):
    """
    get users info (index)
    :param result:
    :param db_name:
    :param _Table_name:
    :return:
    """
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    _Table_name = "0_USERS_INDEX"

    SQL = '''INSERT INTO "{Table_name}" VALUES ( "{time}","{id}", "{username}" ,"{full_name}","{fbid}" ,"{biography}",\
     "{edge_owner_to_timeline_media}" , "{edge_followed_by}" ,"{edge_follow}","{edge_mutual_followed_by}",\
     "{external_url}","{country_block}","{has_ar_effects}","{has_clips}","{has_guides}","{has_channel}",\
     "{highlight_reel_count}","{edge_follow}","{hide_like_and_view_counts}" ,"{is_business_account}",\
     "{is_professional_account}","{is_joined_recently}","{business_address_json}","{business_contact_method}",\
     "{business_email}","{business_phone_number}","{business_category_name}","{category_enum}"\
      ,"{category_name}","{is_private}","{is_verified}","{should_show_category}","{should_show_public_contacts}",\
      "{connected_fb_page}","{pronouns}","{deployment_stage}","{mid_pct}","{seo_category_infos}")'''

    time_now = time.strftime('%Y-%m-%d(%H:%M:%S)', time.localtime())

    SQL2 = SQL.format(Table_name=_Table_name, time=time_now,
                      id=result.id,
                      username=result.username,
                      full_name=result.full_name,
                      fbid=result.fbid,
                      biography=result.biography,
                      edge_owner_to_timeline_media=result.edge_owner_to_timeline_media,
                      edge_followed_by=result.edge_followed_by,
                      edge_follow=result.edge_follow,
                      edge_mutual_followed_by=result.edge_mutual_followed_by,
                      external_url=result.external_url,
                      country_block=result.country_block,
                      has_ar_effects=result.has_ar_effects,
                      has_clips=result.has_clips,
                      has_guides=result.has_guides,
                      has_channel=result.has_channel,
                      highlight_reel_count=result.highlight_reel_count,
                      hide_like_and_view_counts=result.hide_like_and_view_counts,
                      is_business_account=result.is_business_account,
                      is_professional_account=result.is_professional_account,
                      is_joined_recently=result.is_joined_recently,
                      business_address_json=result.business_address_json,
                      business_contact_method=result.business_contact_method,
                      business_email=result.business_email,
                      business_phone_number=result.business_phone_number,
                      business_category_name=result.business_category_name,
                      overall_category_name=result.overall_category_name,
                      category_enum=result.category_enum,
                      category_name=result.category_name,
                      is_private=result.is_private,
                      is_verified=result.is_verified,
                      should_show_category=result.should_show_category,
                      should_show_public_contacts=result.should_show_public_contacts,
                      connected_fb_page=result.connected_fb_page,
                      pronouns=result.pronouns,
                      deployment_stage=result.deployment_stage,
                      mid_pct=result.mid_pct,
                      seo_category_infos=result.seo_category_infos
                      )

    cursor.execute(SQL2)
    # 去掉重複
    # sql_query = "DELETE FROM '{Table_name}' WHERE rowid NOT IN(SELECT MAX(rowid) rowid FROM '{Table_name}' GROUP BY shortcode) "
    # sql_query = sql_query.format(Table_name=_Table_name)
    # cursor.execute(sql_query)
    # 提交
    con.commit()
    cursor.close()
    con.close()
    print("save db over...")


def getTablename(db_name):
    SqlTableQ = "select name from sqlite_master where type='table' order by name;"
    db_name = "Instagram.db"
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    result = cursor.execute(SqlTableQ).fetchall()
    return result[1:]


def serchShortcode(db_name, table_name, shortcode):
    """
    是否有相同post
    :param db_name:
    :return:
    """
    SqlTableQ = """select * from '{table_name}' where shortcode='{shortcode}' """
    SqlTableQ=SqlTableQ.format(table_name=table_name,shortcode=shortcode)
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    result = cursor.execute(SqlTableQ).fetchall()
    return result

def serchNew(db_name, table_name):
    """
    找New post
    :param db_name:
    :return:
    """
    SqlTableQ = """select shortcode from '{table_name}' where is_send='False' ORDER by taken_at_timestamp DESC """
    SqlTableQ=SqlTableQ.format(table_name=table_name)
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    result = cursor.execute(SqlTableQ).fetchall()
    return result

def serchRandom(db_name, table_name):
    """
    隨機post
    :param db_name:
    :return:
    """
    SqlTableQ = """select shortcode from '{table_name}' """
    SqlTableQ=SqlTableQ.format(table_name=table_name)
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    result = cursor.execute(SqlTableQ).fetchall()
    return result

def serchDescription(db_name, table_name,shortcode):
    """
    是否有相同post
    :param db_name:
    :return:
    """
    SqlTableQ = """select edge_media_to_caption from '{table_name}' where shortcode='{shortcode}' ORDER by taken_at_timestamp DESC """
    SqlTableQ=SqlTableQ.format(table_name=table_name,shortcode=str(shortcode))
    # print(SqlTableQ)
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    result = cursor.execute(SqlTableQ).fetchall()
    return result
def serchTime(db_name, table_name,shortcode):
    SqlTableQ = """select taken_at_timestamp from '{table_name}' where shortcode='{shortcode}' ORDER by taken_at_timestamp DESC """
    SqlTableQ=SqlTableQ.format(table_name=table_name,shortcode=str(shortcode))
    # print(SqlTableQ)
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    result = cursor.execute(SqlTableQ).fetchall()
    return result

def updateSendDB(file_name, database_name, _Table_name):
    # 已存
    con = sqlite3.connect(database_name)
    cursor = con.cursor()
    sql_isSendload_pre = "update '{Table_name}' set is_send='Ture' where shortcode = '"
    sql_isSendload_pre = sql_isSendload_pre.format(Table_name=_Table_name)
    sql_isSendload = sql_isSendload_pre + file_name + "'"
    cursor.execute(sql_isSendload)
    con.commit()
    cursor.close()
    con.close()
    print("DB is_send = True")
