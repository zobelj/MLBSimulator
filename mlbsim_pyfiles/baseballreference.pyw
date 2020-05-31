import requests as rq
import xlwings as xl
import time

teams = ['angels', 'astros', 'athletics', 'bluejays', 'braves', 'brewers', 'cardinals', 'cubs', 'diamondbacks', 'dodgers', 'giants', 'indians', 'mariners', 'marlins', 'mets', 'nationals', 'orioles', 'padres', 'phillies', 'pirates', 'rangers', 'rays', 'redsox', 'reds', 'rockies', 'royals', 'tigers', 'twins', 'whitesox', 'yankees']

a = True

excel_app = xl.App(visible=True)
excel_book = excel_app.books.open('Baseball Simulator Helper.xlsx')
sht = excel_book.sheets['Sheet1']

def update():

    for i in range(0,len(teams),1):
        a = rq.get('https://www.fangraphs.com/teams/{}/schedule?season=2017'.format(teams[i]))
        b = a.text
        c = b.split('<div class="team-schedule-table"><table>')[1]  

        for j in range(162):

            d = c.split('</td><td>')[3*j-1]
            e = c.split('</td><td>')[3*j]
            f = e.split('</td>')[0]
            g = f.split('</td>')[0]

            if(i>25):
                asc = 2*i+45
                sht.range('b'+chr(asc)+'1').value = teams[i]
                sht.range('b'+chr(asc+1)+'1').value = teams[i] + '1'
                sht.range('b'+chr(asc)+'2').value = 'R'
                sht.range('b'+chr(asc+1)+'2').value = 'RA'
                sht.range('b'+chr(asc)+str(j+2)).value = d
                sht.range('b'+chr(asc+1)+str(j+2)).value = g
            
            elif(i>12):
                asc = 2*i+71
                sht.range('a'+chr(asc)+'1').value = teams[i]
                sht.range('a'+chr(asc+1)+'1').value = teams[i] + '1'
                sht.range('a'+chr(asc)+'2').value = 'R'
                sht.range('a'+chr(asc+1)+'2').value = 'RA'
                sht.range('a'+chr(asc)+str(j+2)).value = d
                sht.range('a'+chr(asc+1)+str(j+2)).value = g
                
            else:
                asc = 2*i+97
                sht.range(chr(asc)+'1').value = teams[i]
                sht.range(chr(asc+1)+'1').value = teams[i] + '1'
                sht.range(chr(asc)+'2').value = 'R'
                sht.range(chr(asc+1)+'2').value = 'RA'
                sht.range(chr(asc)+str(j+2)).value = d
                sht.range(chr(asc+1)+str(j+2)).value = g

update()
