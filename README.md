# delete_duplicated_wps_addons
wps运行一段时间后，会变得越来越臃肿，各种精简工具也没法清理干净，于是写了一个工具，用于删除wps中过时的addons。
addons的目录是%APPDATA%/kingsoft/wps/addons/pools/win-i386
通过对比版本号，删除比较旧的addons。
1、删除之前没有增加提示，而是直接删除，主要是因为删除没有什么发现不良后果，就算删错了，wps也会重新下载下来
2、个别addons有些特别，比如photo，已经有3这个版本了，还是会重新把2版本的下载下来，由于么有发现什么副作用，也就没管
3、其它运行垃圾还没有发现机制，也就没有搞
