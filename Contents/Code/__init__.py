import sys
from PMS import Plugin, Log, DB, Thread, XML, HTTP, JSON, RSS, Utils
from PMS.MediaXML import MediaContainer, DirectoryItem, PhotoItem

BP_PLUGIN_PREFIX   = "/photos/TheBigPicture"
BP_RSS_FEED        = "http://www.boston.com/bigpicture/index.xml"

####################################################################################################
def Start():
  Plugin.AddRequestHandler(BP_PLUGIN_PREFIX, HandlePhotosRequest, "The Big Picture", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("ImageStream", viewMode="Pictures", contentType="items")

####################################################################################################
def HandlePhotosRequest(pathNouns, count):
  dir = MediaContainer("art-default.jpg", None, "The Big Picture")
  
  if count == 0:
    feed = RSS.Parse(BP_RSS_FEED)
    for item in feed.entries:
        dir.AppendItem(DirectoryItem(Utils.EncodeStringToUrlPath(item.link)+'$'+item.title, item.title, ""))
  elif count == 1:
    (url,title) = pathNouns[0].split('$')
    dir = MediaContainer("art-default.jpg", "ImageStream", "The Big Picture", title)
    url = Utils.DecodeUrlPathToString(url)
    i = 1
    for photo in XML.ElementFromURL(url, True).xpath("//div[@class='bpBoth']"):
      try:
        src = photo.find('img').get('src')
        summary = photo.xpath("div[@class='bpCaption']/text()")[0]
        dir.AppendItem(PhotoItem(src, "Photo %d" % i, summary, None))
        i += 1
      except:
        sys.stderr.write("No image found")

  return dir.ToXML()