from facepy import GraphAPI
import datetime
import random
# import facebook
from datetime import datetime
import psycopg2
#Para escanear todos tus amigos
conexion = psycopg2.connect(database="personas", user="postgres", password="root")
sql = "INSERT INTO public.cuentas(nombre, sexo, telefono,id,email,is_friend_public) values (%s,%s,%s,%s,%s,%s)"
sql_update = "INSERT INTO public.cuentas(nombre, sexo, telefono,id,email) values (%s,%s,%s,%s,%s)"
# sql="INSERT INTO public.cuentas(nombre, sexo, telefono,id) values (%s,%s,%s,%s,)"

#put your email and password 
#generate token here https://b-api.facebook.com/method/auth.login?access_token=237759909591655%25257C0f140aabedfb65ac27a739ed1a2263b1&format=json&sdk_version=2&email=your_email&locale=en_US&password=ypur_passwor&sdk=ios&generate_session_cookies=1&sig=3f555f99fb61fcd7aa0c44f58f522ef6

oauth_token = ''  # Put your User access token here.!!
graph = GraphAPI(oauth_token)
account = 'me'
friend_list = graph.get(account + "/friends?fields=name,gender,mobile_phone,email")
print()
# birthday wishes are as follows
birthday_wishes = ["Life wouldn't be the same without a friend like you. Happy Birthday!",
                   "My best wishes for a furious and voracious day filled with plenty of smile and laughter. Happy Birthday to you!",
                   "May the special day of yours be filled with loving memories full of fun and the company of good friends. Happy Birthday!",
                   "Look for the best and leave behind all the rest. Happy Birthday my friend!",
                   "One year older means one year wiser. The truth is that our company needed an old wise person like you. Happy Birthday my friend"
                   ]
# print(friend_list)
# Get today's day and month
now = datetime.now().strftime("%m-%d")
month_day = now.split('-')
a = 0
b = 0
genero = 'no_se_sabe'
telefono = 'no-registrado'
print(friend_list)

for friend in friend_list['data']:
    b = 0
    a = a + 1
    account = friend['id']
    try:
        friend_list = graph.get(account + "/friends?fields=name,gender,mobile_phone,email")
        print('\r\033[37;1m[\x1b[92m+\033[37;1m] \033[37;1m' + friend['name'])
        if ('gender' in friend and 'mobile_phone' in friend) and 'email' in friend:

            datos = (friend['name'], friend['gender'], friend['mobile_phone'], friend['id'], friend['email'],True)
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()

        # friend_list = graph.get(account + "/friends?fields=name,gender,mobile_phone,email")

        for friend_of_my_friends in friend_list['data']:
            b = b + 1
            try:
                print('\r\033[32;1m[\033[37;1m=\033[32;1m]\033[34;1m Start \033[37;1m>\033[35;1m ' + friend['name'] + '\033[37;1m >\033[35;1m ' + friend_of_my_friends['name'] + " " + str(b))
                datos = (
                friend_of_my_friends['name'], friend_of_my_friends['gender'], friend_of_my_friends['mobile_phone'],
                friend_of_my_friends['id'], friend_of_my_friends['email'],False)
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
                print(a)
            except KeyError as error:
                print("error de key")
            except psycopg2.Error as e:
                print("error de base de datos" + e.pgerror)
                conexion.close()
                conexion = psycopg2.connect(database="personas", user="postgres", password="root")

    except KeyError as error:
        print(error + str(error))
    except psycopg2.Error as e:
        print("error de base de datos" + e.pgerror)
        conexion.close()
        conexion = psycopg2.connect(database="personas", user="postgres", password="root")
    print(a)
