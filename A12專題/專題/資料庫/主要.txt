use lol
CREATE TABLE player (
   accountid varchar(20)not null,
   summonerid varchar(20),
   summoner_name varchar(35),
   crawl varchar(8)
) 

ALTER TABLE player
  ADD PRIMARY KEY (accountid);

CREATE TABLE game (
   gameid varchar(20)not null,
   game_duration int,
   win varchar(7)
) 

ALTER TABLE game
  ADD PRIMARY KEY (gameid);

CREATE TABLE fight (
   gameid varchar(20) NOT NULL,
   accountid varchar(20) NOT NULL,
   teamid varchar(5) , 
   champion nvarchar(20) ,
   lane varchar(10)
) 

ALTER TABLE fight
  ADD PRIMARY KEY (gameid , accountid);

create table eachchamp_winrate (
      accountid varchar(20)not null,
	  champ_name varchar(20)not null,
	  winrate float
)
ALTER TABLE eachchamp_winrate
  ADD PRIMARY KEY (accountid , champ_name);

create table champ_lane (
     champ_name varchar(20) ,
     lane varchar(20)
)

CREATE TABLE champion (
   id varchar(20)not null,
   champ_name varchar(20),
   ) 
ALTER TABLE champion
  ADD PRIMARY KEY (id);

insert into champion values(266, 'Aatrox')
insert into champion values(103, 'Ahri')
insert into champion values(84, 'Akali')
insert into champion values(12, 'Alistar')
insert into champion values(32, 'Amumu')
insert into champion values(34, 'Anivia')
insert into champion values(1, 'Annie')
insert into champion values(523, 'Aphelios')
insert into champion values(22, 'Ashe')
insert into champion values(136, 'AurelionSol')
insert into champion values(268, 'Azir')
insert into champion values(432, 'Bard')
insert into champion values(53, 'Blitzcrank')
insert into champion values(63, 'Brand')
insert into champion values(201, 'Braum')
insert into champion values(51, 'Caitlyn')
insert into champion values(164, 'Camille')
insert into champion values(69, 'Cassiopeia')
insert into champion values(31, 'Chogath')
insert into champion values(42, 'Corki')
insert into champion values(122, 'Darius')
insert into champion values(131, 'Diana')
insert into champion values(119, 'Draven')
insert into champion values(36, 'DrMundo')
insert into champion values(245, 'Ekko')
insert into champion values(60, 'Elise')
insert into champion values(28, 'Evelynn')
insert into champion values(81, 'Ezreal')
insert into champion values(9, 'Fiddlesticks')
insert into champion values(114, 'Fiora')
insert into champion values(105, 'Fizz')
insert into champion values(3, 'Galio')
insert into champion values(41, 'Gangplank')
insert into champion values(86, 'Garen')
insert into champion values(150, 'Gnar')
insert into champion values(79, 'Gragas')
insert into champion values(104, 'Graves')
insert into champion values(120, 'Hecarim')
insert into champion values(74, 'Heimerdinger')
insert into champion values(420, 'Illaoi')
insert into champion values(39, 'Irelia')
insert into champion values(427, 'Ivern')
insert into champion values(40, 'Janna')
insert into champion values(59, 'JarvanIV')
insert into champion values(24, 'Jax')
insert into champion values(126, 'Jayce')
insert into champion values(202, 'Jhin')
insert into champion values(222, 'Jinx')
insert into champion values(145, 'Kaisa')
insert into champion values(429, 'Kalista')
insert into champion values(43, 'Karma')
insert into champion values(30, 'Karthus')
insert into champion values(38, 'Kassadin')
insert into champion values(55, 'Katarina')
insert into champion values(10, 'Kayle')
insert into champion values(141, 'Kayn')
insert into champion values(85, 'Kennen')
insert into champion values(121, 'Khazix')
insert into champion values(203, 'Kindred')
insert into champion values(240, 'Kled')
insert into champion values(96, 'KogMaw')
insert into champion values(7, 'Leblanc')
insert into champion values(64, 'LeeSin')
insert into champion values(89, 'Leona')
insert into champion values(876, 'Lillia')
insert into champion values(127, 'Lissandra')
insert into champion values(236, 'Lucian')
insert into champion values(117, 'Lulu')
insert into champion values(99, 'Lux')
insert into champion values(54, 'Malphite')
insert into champion values(90, 'Malzahar')
insert into champion values(57, 'Maokai')
insert into champion values(11, 'MasterYi')
insert into champion values(21, 'MissFortune')
insert into champion values(62, 'MonkeyKing')
insert into champion values(82, 'Mordekaiser')
insert into champion values(25, 'Morgana')
insert into champion values(267, 'Nami')
insert into champion values(75, 'Nasus')
insert into champion values(111, 'Nautilus')
insert into champion values(518, 'Neeko')
insert into champion values(76, 'Nidalee')
insert into champion values(56, 'Nocturne')
insert into champion values(20, 'Nunu')
insert into champion values(2, 'Olaf')
insert into champion values(61, 'Orianna')
insert into champion values(516, 'Ornn')
insert into champion values(80, 'Pantheon')
insert into champion values(78, 'Poppy')
insert into champion values(555, 'Pyke')
insert into champion values(246, 'Qiyana')
insert into champion values(133, 'Quinn')
insert into champion values(497, 'Rakan')
insert into champion values(33, 'Rammus')
insert into champion values(421, 'RekSai')
insert into champion values(58, 'Renekton')
insert into champion values(107, 'Rengar')
insert into champion values(92, 'Riven')
insert into champion values(68, 'Rumble')
insert into champion values(13, 'Ryze')
insert into champion values(360, 'Samira')
insert into champion values(113, 'Sejuani')
insert into champion values(235, 'Senna')
insert into champion values(147, 'Seraphine')
insert into champion values(875, 'Sett')
insert into champion values(35, 'Shaco')
insert into champion values(98, 'Shen')
insert into champion values(102, 'Shyvana')
insert into champion values(27, 'Singed')
insert into champion values(14, 'Sion')
insert into champion values(15, 'Sivir')
insert into champion values(72, 'Skarner')
insert into champion values(37, 'Sona')
insert into champion values(16, 'Soraka')
insert into champion values(50, 'Swain')
insert into champion values(517, 'Sylas')
insert into champion values(134, 'Syndra')
insert into champion values(223, 'TahmKench')
insert into champion values(163, 'Taliyah')
insert into champion values(91, 'Talon')
insert into champion values(44, 'Taric')
insert into champion values(17, 'Teemo')
insert into champion values(412, 'Thresh')
insert into champion values(18, 'Tristana')
insert into champion values(48, 'Trundle')
insert into champion values(23, 'Tryndamere')
insert into champion values(4, 'TwistedFate')
insert into champion values(29, 'Twitch')
insert into champion values(77, 'Udyr')
insert into champion values(6, 'Urgot')
insert into champion values(110, 'Varus')
insert into champion values(67, 'Vayne')
insert into champion values(45, 'Veigar')
insert into champion values(161, 'Velkoz')
insert into champion values(254, 'Vi')
insert into champion values(112, 'Viktor')
insert into champion values(8, 'Vladimir')
insert into champion values(106, 'Volibear')
insert into champion values(19, 'Warwick')
insert into champion values(498, 'Xayah')
insert into champion values(101, 'Xerath')
insert into champion values(5, 'XinZhao')
insert into champion values(157, 'Yasuo')
insert into champion values(777, 'Yone')
insert into champion values(83, 'Yorick')
insert into champion values(350, 'Yuumi')
insert into champion values(154, 'Zac')
insert into champion values(238, 'Zed')
insert into champion values(115, 'Ziggs')
insert into champion values(26, 'Zilean')
insert into champion values(142, 'Zoe')
insert into champion values(143, 'Zyra')