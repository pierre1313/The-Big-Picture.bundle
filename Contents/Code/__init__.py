BP_PLUGIN_PREFIX   = "/photos/TheBigPicture"
PLUGIN_TITLE       = "The Big Picture"
BP_RSS_FEED        = "http://www.boston.com/bigpicture/index.xml"

ART         = "art-default.jpg"
ICON        = "icon-default.png"

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(BP_PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE, ICON, ART)
  Plugin.AddViewGroup("ImageStream", viewMode="Pictures", mediaType="items")
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

  MediaContainer.art       = R(ART)
  MediaContainer.title1    = PLUGIN_TITLE
  MediaContainer.viewGroup = "InfoList"
  DirectoryItem.thumb      = R(ICON)

####################################################################################################
def MainMenu():
  dir = MediaContainer(viewGroup = "List")
  feed = XML.ElementFromURL(BP_RSS_FEED)
  for item in feed.xpath("//rss//channel//item"):
    description = item.xpath(".//description")[0].text.replace('&gt;','>').replace('&lt','<')
    thumb = HTML.ElementFromString(description).xpath(".//div[@class='bpImageTop']//img")[0].get('src')
    url = item.xpath(".//link")[0].text
    title = item.xpath(".//title")[0].text
    dir.Append(Function(DirectoryItem(HandlePhotos,title,thumb=thumb),url = url, title = title))

  return dir
  
def HandlePhotos(sender, url = "", title = ''):
  dir = MediaContainer(viewGroup = "ImageStream")

  for photo in HTML.ElementFromURL(url).xpath("//div[@class='bpBoth']"):
    try:
      src = photo.xpath('img')[0].get('src')
      summary = photo.xpath("div[@class='bpCaption']/text()")[0]
      dir.Append(PhotoItem(src, title, summary, None))
    except:
      pass
    
  return dir