import cv2
# import pafy

# myvid = pafy.new("https://youtu.be/y6TmFxcVrnI")
# #best = myvid.getbestvideo(preftype="any")
# streams = myvid.streams
# for s in streams:
#     print(s.url)

cap = cv2.VideoCapture("https://manifest.googlevideo.com/api/manifest/hls_playlist/id/y6TmFxcVrnI.3/itag/91/source/yt_live_broadcast/requiressl/yes/ratebypass/yes/live/1/cmbypass/yes/goi/160/sgoap/gir%3Dyes%3Bitag%3D139/sgovp/gir%3Dyes%3Bitag%3D160/hls_chunk_host/r3---sn-nx57ynls.googlevideo.com/ei/N0y0WuKAIYXK-APOorfYCg/playlist_type/DVR/gcr/us/initcwndbps/12390/mm/32/mn/sn-nx57ynls/ms/lv/mv/m/pl/20/dover/10/keepalive/yes/mt/1521765313/ip/75.147.184.233/ipbits/0/expire/1521787031/sparams/ip,ipbits,expire,id,itag,source,requiressl,ratebypass,live,cmbypass,goi,sgoap,sgovp,hls_chunk_host,ei,playlist_type,gcr,initcwndbps,mm,mn,ms,mv,pl/signature/226BE41047EBDE0432F579920A72A9E65FD6D59E.1418C07707AD4712BA6F6DF187E0F4D3725453D4/key/dg_yt0/playlist/index.m3u8")
while True:
    ret, frame = cap.read()

    cv2.imshow('frame', frame)
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()