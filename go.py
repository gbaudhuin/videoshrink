import worker
# import mediainfo
# mediainfo.MediaInfo('C:\\Users\\baudh\\OneDrive\\Photos\\2012\\2012-04-28 - Port bourgenay\\Zoo\\00000.MTS')
# quit()
# import converter
# conv = converter.Converter('C:\\Users\\baudh\\OneDrive\\Photos\\2012\\2012-04-28 - Port bourgenay\\Zoo\\00000.MTS',
#                     'out/test.mp4')
# conv.run()
# quit()
# import mediatask
# m = mediatask.MediaTask("C:\\Users\\baudh\\OneDrive\\Pictures\\Camera Roll\\20200404_183822.mp4")
# m.run()
# quit()
_worker = worker.Worker()

totalsizeMb = _worker.get_total_size() / (1024*1024)
print("Total size : {:0.1f} Mb".format(totalsizeMb))
#print(_worker.next())
_worker.run()
