# Unreal-LiveLink-for-Blender

The Blender-Unreal Live Link add-on makes it possible to stream data from Blender to Unreal in real time. Saving your production time of manually importing animations you have created inside Blender.

Features:

1) Simple Editor addon with simple UI.

2) Supports both static and skeletal mesh.

3) Multiple subjects can be registered at a time. That is you can add multiple armatures and can switch control between them.

4) You can stream either single subject data or stream multiple subjects data simultaneously, giving you control over multiple

multiple subjects present in your blender viewport.

![Alt text](https://github.com/Viga-Entertainment-Technology/Unreal-LiveLink-for-Blender/blob/main/Screenshots/BlenderUnrealLiveLink.gif)

How to install?

1) Download the given addon file "BlenderLiveLinkAddon.py".
2) Open Blender go to Edit->Preferences->Add-Ons. Click on the install button and locate the downloaded addon.
3) Search for “LiveLink” in the add-ons section and tick the checkbox to enable the plugin.
3) The add on will be installed and you can access from editor the LiveLink Tab.

For more instructions and the setup in unreal engine, refer to the instructions given [here](https://vigaet-my.sharepoint.com/:w:/p/shreyas/Eab3ieXYF_JDvMs_51-H3osByFEwrzTcrqj8wMJMO95DOA).

Update Note:
1) Updated UI.
2) Viewport color will no longer change.
3) Subjects will remain registered until you remove those subjects from the list.
5) Stop live link button has been added.


Bug Fixed:
1) Key error due to subject not being found has been fixed.
2) Live link will no longer stop when you press ESC key or click right mouse button.
