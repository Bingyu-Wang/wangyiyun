--删除纯音乐（分别删除95130，2926，594，2413首歌曲）
use wangyiyun
SET SQL_SAFE_UPDATES=0
delete from lyric where lyric=' '
delete from lyric where lyric like '%纯音乐%'
delete from lyric where lyric like '%暂无歌词%'
delete FROM lyric where CHAR_LENGTH(lyric)<40;
