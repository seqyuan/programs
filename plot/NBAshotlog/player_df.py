import requests
import pandas as pd

def request_df(PlayerID):
	shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?AheadBehind=&'\
					 'CFID=&CFPARAMS=&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGA'\
					 '&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GROUP_ID=&GameEventID='\
					 '&GameID=&GameSegment=&GroupID=&GroupMode=&GroupQuantity=5&LastNGames=0&LeagueID=00'\
					 '&Location=&Month=0&OnOff=&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID={PlayerID}'\
					 '&PlayerID1=&PlayerID2=&PlayerID3=&PlayerID4=&PlayerID5=&PlayerPosition=&PointDiff=&Position='\
					 '&RangeType=0&RookieYear=&Season={Season}&SeasonSegment=&SeasonType={SeasonType}'\
					 '&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference='\
					 '&VsDivision=&VsPlayerID1=&VsPlayerID2=&VsPlayerID3=&VsPlayerID4=&VsPlayerID5='\
					 '&VsTeamID='.format(PlayerID=PlayerID,Season='2017-18',SeasonType='Regular+Season')

	header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'\
							  ' Chrome/62.0.3202.94 Safari/537.36'}

	response = requests.get(shot_chart_url,headers=header)
	# headers是模拟浏览器访问行为，现在没有这一项获取不到数据

	headers = response.json()['resultSets'][0]['headers']
	shots = response.json()['resultSets'][0]['rowSet']
	shot_df = pd.DataFrame(shots, columns=headers)

	outdf = shot_df[shot_df['LOC_Y']==0][['LOC_X','LOC_Y','SHOT_DISTANCE']]
	return outdf

playersID = [202691,203078,202331,2544,201939]

df = pd.DataFrame()
for i in playersID:
	df2 = request_df(i)
	if df.shape[0] == 0:
		df = df2
	else:
		df = pd.concat([df,df2],axis=0)

aa = df[df['SHOT_DISTANCE'] >1]
aa['c'] = df['LOC_X']/df['SHOT_DISTANCE']
print (aa)

