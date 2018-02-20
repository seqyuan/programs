import requests
import pandas as pd

shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?AheadBehind=&'\
				 'CFID=&CFPARAMS=&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGA'\
				 '&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GROUP_ID=&GameEventID='\
				 '&GameID=&GameSegment=&GroupID=&GroupMode=&GroupQuantity=5&LastNGames=0&LeagueID=00'\
				 '&Location=&Month=0&OnOff=&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID={PlayerID}'\
				 '&PlayerID1=&PlayerID2=&PlayerID3=&PlayerID4=&PlayerID5=&PlayerPosition=&PointDiff=&Position='\
				 '&RangeType=0&RookieYear=&Season={Season}&SeasonSegment=&SeasonType={SeasonType}'\
				 '&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference='\
				 '&VsDivision=&VsPlayerID1=&VsPlayerID2=&VsPlayerID3=&VsPlayerID4=&VsPlayerID5='\
				 '&VsTeamID='.format(PlayerID=201935,Season='2017-18',SeasonType='Regular+Season')
header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'\
						  ' Chrome/62.0.3202.94 Safari/537.36'}
response = requests.get(shot_chart_url,headers=header)
# headers是模拟浏览器访问行为，

headers = response.json()['resultSets'][0]['headers']
shots = response.json()['resultSets'][0]['rowSet']
shot_df = pd.DataFrame(shots, columns=headers)

# View the head of the DataFrame and all its columns
from IPython.display import display
with pd.option_context('display.max_columns', None):
	display(shot_df.head())
# Or 
shot_df.to_excel('outfile.xlsx',index=True,header=True)