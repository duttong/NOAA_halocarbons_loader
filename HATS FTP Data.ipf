#pragma rtGlobals=3		// Use modern global access method and strict wave access.
#include "macros-geoff"
#include "macros-utilities"
#pragma IgorVersion=6.3
#pragma version=1.2			// 1.2 added PERSEUS

// Added five HFCs for the M2 MSD instrument.  150622 GSD
// Added F11 for MSD  180611
// Added PERSEUS to the MSD loader.  190624

// combined data sets
strconstant kCOMBmols = "N2O;SF6;F11;F12;F113;MC;CCl4;"

// in situ programs
strconstant kRITSmols = "N2O;F11;F12;MC;CCl4;"
strconstant kCATSmols = "N2O;SF6;F11;F12;F113;MC;CCl4;h1211;HCFC22;HCFC142b;CH3Cl;"

// flasks programs
strconstant kOLDGCmols = "N2O;F11;F12;"
strconstant kOTTOmols = "N2O;SF6;F11;F12;F113;MC;CCl4;"
// M3 mols
strconstant kMSDmols = "F11;F12;F113;HCFC22;HCFC141b;HCFC142b;HFC134A;HFC152A;HFC227ea;HFC365mfc;OCS;CH3CCl3;CH2Cl2;C2Cl4;h1211;h2402;CH3Br;CH3Cl;"
// added PERSEUS 190624, added HFOs 201028
strconstant kPERSEUSmols = "h1301;HFC125;HFC143a;HFC32;C2H6;C3H8;CF4;HFC236fa;NF3;PFC116;SO2F2;HFO1234yf;HFO1234ze;"
strconstant kMSDcatsmols = "F11;F113;HCFC22;HCFC142b;COS;CH3CCl3;h1211;CH3Br;CH3Cl;"

// HATS sampling stations
strconstant kHATSsites = "alt;brw;lef;nwr;kum;mlo;smo;cgo;psa;spo;hfm;mhd;thd;ush;sum;"  // changed tdf to ush 190609


Menu "GMD_FTP"
	"(in situ data"
	"Load RITS Data"
	"Load CATS Data"
	"-"
	"(Flask Data"
	"Load Old GC Data"
	"Load OTTO Data"
	"Load MSD Data"
	"-"
	"(Combined Data"
	"Load Combined Data"
	"-"
	"Remove Displayed Graphs"
end

function LoadRITSdata([mol, freq, useDF, plot])
	string mol, freq
	variable useDF, plot

	SVAR /Z Smol = root:S_mol
	SVAR /Z Sfreq = root:S_freq
	NVAR /Z GuseDF = root:G_useDF
	NVAR /Z Gplot = root:G_plot	
	if (!SVAR_exists(Smol))
		String /G root:S_mol = "N2O"
		String /G root:S_freq = "monthly"
		Variable /G root:G_useDF = 2
		Variable /G root:G_plot = 2
		SVAR /Z Smol = root:S_mol
		SVAR /Z Sfreq = root:S_freq
		NVAR /Z GuseDF = root:G_useDF
		NVAR /Z Gplot = root:G_plot	
	endif		
	if (!SVAR_exists(Sfreq))
		String /G root:S_freq = "monthly"
		SVAR /Z Sfreq = root:S_freq
	endif
	
	if (ParamIsDefault(useDF))
		useDF=GuseDF
		Prompt useDF, "Use RITS data folder?", popup, "No;Yes"
	endif
	if (ParamIsDefault(plot))
		plot=Gplot
		Prompt plot, "Make figures?", popup, "No;Yes"
	endif
	if (ParamIsDefault(freq))
		freq=Sfreq
		Prompt freq, "Frequency:", popup, "hourly;daily;monthly;global"
	endif
	if (ParamIsDefault(mol))
		mol=Smol
		Prompt mol, "Which molecule?", popup, kRITSmols
		DoPrompt "Load RITS data from GMD ftp site", mol, freq, useDF, plot
		if (V_flag)
			return 0
		endif
	endif

	Gplot = plot
	GuseDF=useDF
	Sfreq=freq
	Smol=mol
	plot = plot==2
	useDF = useDF==2

	// use data folder for storage
	if (useDF)
		NewDataFolder /O/S root:RITS
	endif
			
	if (cmpstr(freq, "global")==0)
		GlobalClipLoader("RITS", mol, freq)
	else
		ClipLoader("RITS", mol, freq)
	endif
			
	SetDataFolder root:

end

function LoadCATSdata([mol, freq, useDF, plot])
	string mol, freq
	variable useDF, plot

	SVAR /Z Smol = root:S_mol
	SVAR /Z Sfreq = root:S_freq
	NVAR /Z GuseDF = root:G_useDF
	NVAR /Z Gplot = root:G_plot	
	if (!SVAR_exists(Smol))
		String /G root:S_mol = "N2O"
		String /G root:S_freq = "monthly"
		Variable /G root:G_useDF = 2
		Variable /G root:G_plot = 2
	endif		
	
	if (ParamIsDefault(useDF))
		useDF=GuseDF
		Prompt useDF, "Use CATS data folder?", popup, "No;Yes"
	endif
	if (ParamIsDefault(plot))
		plot=Gplot
		Prompt plot, "Make figures?", popup, "No;Yes"
	endif
	if (ParamIsDefault(freq))
		freq=Sfreq
		Prompt freq, "Frequency:", popup, "hourly;daily;monthly;global"
	endif
	if (ParamIsDefault(mol))
		mol=Smol
		Prompt mol, "Which molecule?", popup, kCATSmols
		DoPrompt "Load CATS data from GMD ftp site", mol, freq, useDF, plot
		if (V_flag)
			return 0
		endif
	endif

	Gplot = plot
	GuseDF=useDF
	Sfreq=freq
	Smol=mol
	plot = plot==2
	useDF = useDF==2

	// use data folder for storage
	if (useDF)
		NewDataFolder /O/S root:CATS
	endif
	
	if (cmpstr(freq, "global")==0)
		GlobalClipLoader("CATS", mol, freq)
	else
		ClipLoader("CATS", mol, freq)
	endif
			
	SetDataFolder root:

end

function LoadCombinedData([mol, useDF, plot])
	string mol
	variable useDF, plot

	SVAR /Z Smol = root:S_mol
	NVAR /Z GuseDF = root:G_useDF
	NVAR /Z Gplot = root:G_plot	
	if (!SVAR_exists(Smol))
		String /G root:S_mol = "N2O"
		Variable /G root:G_useDF = 2
		Variable /G root:G_plot = 2
		SVAR /Z Smol = root:S_mol
		NVAR /Z GuseDF = root:G_useDF
		NVAR /Z Gplot = root:G_plot	
	endif		
	
	if (ParamIsDefault(useDF))
		useDF=GuseDF
		Prompt useDF, "Use Comb data folder?", popup, "No;Yes"
	endif
	if (ParamIsDefault(plot))
		plot=Gplot
		Prompt plot, "Make figures?", popup, "No;Yes"
	endif
	if (ParamIsDefault(mol))
		mol=Smol
		Prompt mol, "Which molecule?", popup, kCOMBmols
		DoPrompt "Load HATS combined data from GMD ftp site", mol, useDF, plot
		if (V_flag)
			return 0
		endif
	endif

	Gplot = plot
	GuseDF=useDF
	Smol=mol
	plot = plot==2
	useDF = useDF==2

	// use data folder for storage
	if (useDF)
		NewDataFolder /O/S root:Comb
	endif
	
	ClipLoader_Comb(mol)
			
	SetDataFolder root:

end

function LoadOldGCdata([mol, freq, useDF, plot])
	string mol, freq
	variable useDF, plot

	SVAR /Z Smol = root:S_mol
	SVAR /Z Sfreq = root:S_freq
	NVAR /Z GuseDF = root:G_useDF
	NVAR /Z Gplot = root:G_plot	
	if (!SVAR_exists(Smol))
		String /G root:S_mol = "N2O"
		String /G root:S_freq = "monthly"
		Variable /G root:G_useDF = 2
		Variable /G root:G_plot = 2
	endif		
	
	if (ParamIsDefault(useDF))
		useDF=GuseDF
		Prompt useDF, "Use OldGC data folder?", popup, "No;Yes"
	endif
	if (ParamIsDefault(plot))
		plot=Gplot
		Prompt plot, "Make figures?", popup, "No;Yes"
	endif
	if (ParamIsDefault(freq))
		freq=Sfreq
		Prompt freq, "Frequency:", popup, "monthly"
	endif
	if (ParamIsDefault(mol))
		mol=Smol
		Prompt mol, "Which molecule?", popup, kOLDGCmols
		DoPrompt "Load OldGC data from GMD ftp site", mol, freq, useDF, plot
		if (V_flag)
			return 0
		endif
	endif

	Gplot = plot
	GuseDF=useDF
	Sfreq=freq
	Smol=mol
	plot = plot==2
	useDF = useDF==2

	// use data folder for storage
	if (useDF)
		NewDataFolder /O/S root:OldGC
	endif
	
	ClipLoader("OldGC", mol, freq)
			
	SetDataFolder root:

end

function LoadOTTOdata([mol, freq, useDF, plot])
	string mol, freq
	variable useDF, plot

	SVAR /Z Smol = root:S_mol
	if (!SVAR_exists(Smol))
		String /G root:S_mol = "N2O"
		String /G root:S_freq = "monthly"
		Variable /G root:G_useDF = 2
		Variable /G root:G_plot = 2
	endif		
	SVAR /Z Smol = root:S_mol
	SVAR /Z Sfreq = root:S_freq
	NVAR /Z GuseDF = root:G_useDF
	NVAR /Z Gplot = root:G_plot	
	
	if (ParamIsDefault(useDF))
		useDF=GuseDF
		Prompt useDF, "Use OTTO data folder?", popup, "No;Yes"
	endif
	if (ParamIsDefault(plot))
		plot=Gplot
		Prompt plot, "Make figures?", popup, "No;Yes"
	endif
	if (ParamIsDefault(freq))
		freq=Sfreq
		Prompt freq, "Frequency:", popup, "monthly;global"
	endif
	if (ParamIsDefault(mol))
		mol=Smol
		Prompt mol, "Which molecule?", popup, kOTTOmols
		DoPrompt "Load OTTO data from GMD ftp site", mol, freq, useDF, plot
		if (V_flag)
			return 0
		endif
	endif

	Gplot = plot
	GuseDF=useDF
	Sfreq=freq
	Smol=mol
	plot = plot==2
	useDF = useDF==2

	// use data folder for storage
	if (useDF)
		NewDataFolder /O/S root:OTTO
	endif
	
	if (cmpstr(freq, "global")==0)
		GlobalClipLoader("OTTO", mol, freq)
	else
		ClipLoader("OTTO", mol, freq)
		// filter some very low CCl4 data at PSA.  140430 
		if (cmpstr(mol, "CCl4")==0)
			wave MM = CCl4ottoSUMm
			lowchop(MM, 60)
			wave MM = CCl4ottoPSAm
			lowchop(MM, 60)
		endif
	endif
			
	SetDataFolder root:

end


function LoadMSDdata([mol, freq, useDF, plot])
	string mol, freq
	variable useDF, plot

	SVAR /Z Smol = root:S_mol
	if (!SVAR_exists(Smol))
		String /G root:S_mol = "HCFC22"
		String /G root:S_freq = "pairs"
		Variable /G root:G_useDF = 2
		Variable /G root:G_plot = 2
	endif		
	SVAR /Z Smol = root:S_mol
	SVAR /Z Sfreq = root:S_freq
	NVAR /Z GuseDF = root:G_useDF
	NVAR /Z Gplot = root:G_plot	
	
	if (ParamIsDefault(useDF))
		useDF=GuseDF
		Prompt useDF, "Use MSD data folder?", popup, "No;Yes"
	endif
	if (ParamIsDefault(plot))
		plot=Gplot
		Prompt plot, "Make figures?", popup, "No;Yes"
	endif
	if (ParamIsDefault(freq))
		freq=Sfreq
		Prompt freq, "Frequency:", popup, "pairs"
	endif
	if (ParamIsDefault(mol))
		mol=Smol
		Prompt mol, "Which molecule?", popup, kMSDmols+";"+kPERSEUSmols
		DoPrompt "Load MSD flask data from GMD ftp site", mol, freq, useDF, plot
		if (V_flag)
			return 0
		endif
	endif

	Gplot = plot
	GuseDF=useDF
	Sfreq=freq
	Smol=mol
	plot = plot==2
	useDF = useDF==2

	// use data folder for storage
	if (useDF)
		NewDataFolder /O/S root:MSD
	endif
	
	// The G_perseus global variable
	Variable /G root:G_perseus = 0
	if (FindListItem(mol, kPERSEUSmols) != -1)
		Variable /G root:G_perseus = 1
	endif
	
	ClipLoader_MSD(mol, freq)
			
	SetDataFolder root:

end




// Loads RITS, CATS, OldGC, OTTO data from clipboard
function ClipLoader(prog, mol, freq)
	string prog, mol, freq

	Variable i
	String urlStr = GMD_HATS_FTPurl(prog, mol, freq)
	String file, files = ReturnFilesInFTPfolder(urlStr)
	String site, Tstr, response = ""
	
	NVAR /Z Gplot = root:G_plot
	
	if (ItemsInList(files) < 1)
		Print "No files found at " + urlStr
		return 0
	endif
	
	for(i=0; i<ItemsInList(files); i += 1)
		file = StringFromList(i, files)
		site = file[0,2]
		response = FetchURL(urlStr+file)
		PutScrapText response
		LoadWave/G/W/A/O "Clipboard"
		Tstr = TimeWave(prog, mol, freq, site)
		if (Gplot==2)
			Wave m = $mol + prog + site + "m"
			Wave T = $Tstr
			Note m, "From file: " + file
			Note T, "From file: " + file
			QuickFigure(m, t, site, mol, freq, prog)
		endif
	endfor
end



// LoadsMSD flask data from clipboard
// updated 121101 to read new MSD files
// updated for PERSEUS  190624
function ClipLoader_MSD(mol, freq)
	string mol, freq

	Variable i
	NVAR PR1 = root:G_perseus
	String urlStr = GMD_HATS_FTPurl("MSD", mol, freq)
	String file, files = ReturnFilesInFTPfolder(urlStr), matched_file
	String Tstr, response = ""
	
	// mol:filename keys
	string matched = "h1211:HAL1211,h1301:H-1301,h2402:Hal2402,hfc152a:hf152a,hfc134a:hfc134a,hfc125:HFC-125,"
	matched += "hfc143a:HFC-143a,hfc227ea:HFC-227ea,hfc32:HFC-32,hfc365mfc:HFC-365mfc,c2h6:C2H6,c3h8:C3H8,"
	matched += "cf4:CF4,hfc236fa:HFC-236fa,nf3:NF3,pfc116:PFC-116,so2f2:SO2F2,hfo1234yf:HFO-1234yf,hfo1234ze:HFO-1234ze"
	
	if (ItemsInList(files) < 1)
		Print "No files found at " + urlStr
		return 0
	endif

	// steps through the file list to find the file that matches the molecule.
	for(i=0; i<ItemsInList(files); i += 1)
		file = StringFromList(i, files)
		if ((strsearch(file, "GCMS_flask.txt", 0) > -1) || (strsearch(file, "MS_flask.txt", 0) > -1))
			matched_file = StringByKey(mol, matched, ":", ",")
			if ((strlen(matched_file) == 0) || (strsearch(file, matched_file, 0) > -1))
				print urlStr, file, mol
				ClipLoader_MSDsub(urlStr, file, mol, freq)
				break
			endif
		endif
	endfor
	
end

function ClipLoader_MSDsub(urlStr, file, mol, freq)
	string urlStr, file, mol, freq

	string response = FetchURL(urlStr+file)
	response = ReplaceString("\r\n", response, "\r")
	PutScrapText response
	if (cmpstr(freq, "pairs") == 0)
		MSDsplit_sites(mol, file)
	else
		MSDsplit_global(mol, file)
	endif
end

function ClipLoader_MSDsub_clipped(urlStr, file, mol, freq)
	string urlStr, file, mol, freq

	//string response = FetchURL(urlStr+file)
	string response = GetScrapText()  // use this for manually loading a data file from clipboard
	response = ReplaceString("\r\n", response, "\r")
	PutScrapText response
	if (cmpstr(freq, "pairs") == 0)
		MSDsplit_sites(mol, file)
	else
		MSDsplit_global(mol, file)
	endif
end

// LoadsMSD flask data from clipboard
function ClipLoader_Comb(mol)
	string mol

	Variable i
	String urlStr = GMD_HATS_FTPurl("combined", mol, "")
	String file, files = ReturnFilesInFTPfolder(urlStr)
	String Tstr, response = ""

	NVAR /Z Gplot = root:G_plot
		
	if (ItemsInList(files) < 1)
		Print "No files found at " + urlStr
		return 0
	endif
	
	string InsPre = "HATS"
	if (cmpstr(mol, "N2O")==0)
		InsPre = "GMD"
	endif
	if (cmpstr(mol, "SF6")==0)
		InsPre = "GMD"
	endif
	
	for(i=0; i<ItemsInList(files); i += 1)
		file = StringFromList(i, files)
		if (strsearch(file, ".txt", 0) > -1)
			response = FetchURL(urlStr+file)
			PutScrapText response
			LoadWave/G/W/A/O "Clipboard"
			Wave YYYY= $InsPre + "_" + mol + "_YYYY"
			Wave MM = $InsPre + "_" + mol + "_MM"
			String NHstr = InsPre + "_NH_" + mol
			String SHstr = InsPre + "_SH_" + mol
			String GLstr = InsPre + "_Global_" + mol 
			String TTstr = InsPre + "_" + mol + "_TimeG"
			
			Make /O/D/N=(numpnts(YYYY)) $TTstr/Wave=TimeG
			TimeG = date2secs(YYYY, MM, 15)
			SetScale d 0,0,"dat", timeG
			
			if (Gplot==2)
				String win = "Comb_" + mol + "_globalmeans"
				DoWindow /K $win
				Display /K=1 $NHstr, $GLstr, $SHstr vs TimeG
				DoWindow /C $win
	
				ModifyGraph rgb($NHstr)=(0,0,60000)
				ModifyGraph rgb($GLstr)=(8000,8000,8000)
			
				SetAxis/A/N=1 left
				SetAxis/A/N=1 bottom
				
				Label left InsPre+" Global Mean " + mol
				Label bottom "Date"			
			endif
		endif
	endfor
end


// takes MSD file loaded in clipboard and splits out individual sites
//function MSDsplit_Sites_oldfile(mol, file)
	string mol, file

	String c1, c2, c3
	Variable i, si
	String site, grepstr
	
	NVAR /Z Gplot = root:G_plot

	// look for all sites in Clipboard file
	For(si=0; si<ItemsInList(kHATSsites); si+=1)
		site = (StringFromList(si, kHATSsites))

		Sprintf grepstr, "^%s\\s\\d+.\\d+\\s", site
		Make /FREE/T/O/N=0 tmpwv
		Grep/E=grepstr "Clipboard" as tmpwv
		
		if (numpnts(tmpwv) > 0)
			Print "Processing MSD:  " + mol + " at " + UpperStr(site)
			String decstr = mol + "msd" + UpperStr(site) + "dec"
			String mrstr = mol + "msd" + UpperStr(site) + "m"
			String sdstr = mol + "msd" + UpperStr(site) + "sd"
			String datestr = mol + "msd" + UpperStr(site) + "_timeM"
			
			Make /o/d/n=(numpnts(tmpwv)) $decstr/WAVE=dec, $datestr/WAVE=timeM
			Make /o/n=(numpnts(tmpwv)) $mrstr/WAVE=mr, $sdstr/WAVE=sd
			
			for(i=0; i<numpnts(tmpwv); i+=1)
				SplitString /E="[a-z]+\\s(\\d*.\\d*)\\s(\\d*.\\d*)\\s(\\d*.\\d*)" tmpwv[I], c1, c2, c3
				dec[i] = str2num(c1)
				mr[i] = str2num(c2)
				sd[i] = str2num(c3)	
			endfor
			
			Note dec, "From file: " + file
			Note mr, "From file: " + file
			Note sd, "From file: " + file
			Note timeM, "From file: " + file
		
			timeM = decday2secs(dec)
			SetScale d 0,0,"dat", timeM
			
			if (Gplot == 2)
				QuickFigure(mr, timeM, site, mol, "monthly", "MSD")
			endif
			
		endif
	endfor

end

// new file formate 121101
function MSDsplit_Sites(mol, file)
	string mol, file

	String c1, c2, c3
	Variable i, si
	String site, grepstr
	
	NVAR /Z Gplot = root:G_plot
	NVAR PR1 = root:G_perseus

	// look for all sites in Clipboard file
	For(si=0; si<ItemsInList(kHATSsites); si+=1)
		site = (StringFromList(si, kHATSsites))

		Sprintf grepstr, "^%s\\s\\d+.\\d+\\s", site
		if (PR1==1)
			Sprintf grepstr, "^\\s+%s\\s+\\d+.\\d+\\s", UpperStr(site)
		endif
		Make /FREE/T/O/N=0 tmpwv
		Grep/E=grepstr "Clipboard" as tmpwv
		
		if (numpnts(tmpwv) > 0)
			//Print "Processing MSD:  " + mol + " at " + UpperStr(site)
			String decstr = mol + "msd" + UpperStr(site) + "dec"
			String mrstr = mol + "msd" + UpperStr(site) + "m"
			String sdstr = mol + "msd" + UpperStr(site) + "sd"
			String datestr = mol + "msd" + UpperStr(site) + "_timeM"
			
			Make /o/d/n=(numpnts(tmpwv)) $decstr/WAVE=dec, $datestr/WAVE=timeM
			Make /o/n=(numpnts(tmpwv)) $mrstr/WAVE=mr, $sdstr/WAVE=sd
			
			for(i=0; i<numpnts(tmpwv); i+=1)
				if (PR1==1)		// Perseus data file
					string line = TrimString(tmpwv[I],1)
					SplitString /E="^[A-Z]+\\s(\\d*.\\d*)\\s\\d{8}\\s\\d{2}:\\d{2}\\s\\S+\\s\\S+\\s(\\d*.\\d*)\s+(\\d*.\\d*)" line, c1, c2, c3
					// check to see if the data has been flagged.
					if ((strsearch(line, "<", 0) > -1) || (strsearch(line, ">", 0) > -1))
						c2 = "Nan"
						c3 = "Nan"
					endif
				else
					// Montzka data file
					SplitString /E="[a-z]+\\s(\\d*.\\d*)\\s\\d{8}\\s\\d{4}\\s\\S+\\s\\S+\\s(\\d*.\\d*)\\s(\\d*.\\d*)" tmpwv[I], c1, c2, c3
				endif
				dec[i] = str2num(c1)
				mr[i] = str2num(c2)
				sd[i] = str2num(c3)	
			endfor
			
			Note dec, "From file: " + file
			Note mr, "From file: " + file
			Note sd, "From file: " + file
			Note timeM, "From file: " + file
			
			// some MSD is not sorted?  eg h1301 file\\
			sort dec, dec, mr, sd
			mr = SelectNumber(mr == 0.0, mr, nan)		// some MSD data is at 0.0?  GSD 150628 
			mr = SelectNumber(mr < -10, mr, nan)			// set negative numbers to nan
		
			timeM = decday2secs(dec)
			SetScale d 0,0,"dat", timeM
			
			if (Gplot == 2)
				QuickFigure(mr, timeM, site, mol, "monthly", "MSD")
			endif
			
		endif
	endfor

end


// takes MSD file loaded in clipboard and splits out hemispher and global data
function MSDsplit_Global(mol, file)
	string mol, file

	String c1, c2, c3, c4
	Variable i, si
	String site, grepstr
	
	NVAR /Z Gplot = root:G_plot

	Sprintf grepstr, "^\\d\\d[A-Za-z]{3}\\s"
	Make /FREE/T/O/N=0 tmpwv
	Grep/E=grepstr "Clipboard" as tmpwv
	
	if (numpnts(tmpwv) > 0)
		Print "Processing MSD:  " + mol + " global means"
		String decstr = mol + "msd_decG"
		String SHstr = mol + "msd_SH"
		String NHstr = mol + "msd_NH"
		String GLstr = mol + "msd_GL"
		String datestr = mol + "msd_timeG"
		
		//Make /o/t/n=(numpnts(tmpwv)) $txtdstr/WAVE=txtdate
		Make /o/d/n=(numpnts(tmpwv)) $decstr/WAVE=dec, $datestr/WAVE=timeG
		Make /o/n=(numpnts(tmpwv)) $SHstr/WAVE=SH, $NHstr/WAVE=NH, $GLstr/WAVE=GL
		
		for(i=0; i<numpnts(tmpwv); i+=1)
			 SplitString /E="\\d\\d[A-Za-z]{3}\\s(\\d*.\\d*)\\s(\\d*.\\d*)\\s(\\d*.\\d*)\\s(\\d*.\\d*)" tmpwv[i], c1, c2, c3, c4
			dec[i] = str2num(c1)
			SH[i] = str2num(c2)
			NH[i] = str2num(c3)
			GL[i] = str2num(c4)
		endfor

		Note dec, "From file: " + file
		Note SH, "From file: " + file
		Note NH, "From file: " + file
		Note GL, "From file: " + file
		Note timeG, "From file: " + file
		
		timeG = decday2secs(dec)
		SetScale d 0,0,"dat", timeG
		
		if (Gplot == 2)
			String win = "MSD_" + mol + "_globalmeans"
			DoWindow /K $win
			Display /K=1 NH, GL, SH vs TimeG
			DoWindow /C $win

			ModifyGraph rgb($NHstr)=(0,0,60000)
			ModifyGraph rgb($GLstr)=(8000,8000,8000)
		
			SetAxis/A/N=1 left
			SetAxis/A/N=1 bottom
			
			Label left "MSD Global Mean " + mol
			Label bottom "Date"			
		endif
		
	endif

end



// handles RITS And CATS global data files
function GlobalClipLoader(prog, mol, freq)
	string prog, mol, freq

	Variable i
	String urlStr = GMD_HATS_FTPurl(prog, mol, freq)
	String file, files = ReturnFilesInFTPfolder(urlStr)
	String Tstr, response = ""
	
	NVAR /Z Gplot = root:G_plot
	
	if (ItemsInList(files) < 1)
		Print "No files found at " + urlStr
		return 0
	endif
	
	for(i=0; i<ItemsInList(files); i += 1)
		file = StringFromList(i, files)
		response = FetchURL(urlStr+file)
		PutScrapText response
		LoadWave/G/W/A/O "Clipboard"
		//LoadWave/J/W/A/O/K=0/V={"\t, "," $",0,0}/L={WaveNameRow,WaveNameRow+1,0,0,0} "Clipboard"
		
		/// CATS files use "insitu" in their wavenames
		if (cmpstr(prog, "CATS") == 0)
			prog = "insitu"
		endif

		Wave YYYY = $prog + "_" + mol + "_YYYY"
		Wave MM = $prog + "_" + mol + "_MM"
		Tstr = prog + "_" + mol + "_" + "_timeG"
		Make /o/d/n=(numpnts(YYYY))  $Tstr/WAVE=T
		T = date2secs(YYYY, MM, 15)					// roughly the center of the month
		SetScale d 0,0,"dat", T

		if (Gplot==2)
			string gstr = prog + "_global_" + mol
			string nstr = prog + "_NH_" + mol
			Wave g=$gstr
			Wave n=$nstr
			Wave s = $prog + "_SH_" + mol

			if (cmpstr(prog, "insitu")==0)
				prog = "CATS"
			endif
			string win = prog + "_" + mol + "_globalmeans"
			DoWindow /K $win
			Display /K=1 n, g, s vs T
			DoWindow /C $win

			ModifyGraph rgb($nstr)=(0,0,60000)
			ModifyGraph rgb($gstr)=(8000,8000,8000)
		
			SetAxis/A/N=1 left
			SetAxis/A/N=1 bottom
			
			Label left prog + " Global Mean " + mol
			Label bottom "Date"			
		endif
	endfor
end

// function constructs a ftp url 
function/S GMD_HATS_FTPurl(prog, mol, freq)
	string prog, mol, freq

	string baseurl = "ftp://ftp.cmdl.noaa.gov/hats/", url = ""
	string progloc
	
	strswitch (mol)
		case "N2O":
			url += "n2o/"
			break
		case "SF6":
			url += "sf6/"
			break

		// CFCs
		case "F11":
			url += "cfcs/cfc11/" 
			break
		case "F12":
			url += "cfcs/cfc12/"
			break
		case "F113":
			url += "cfcs/cfc113/"
			break
			
		// Solvents
		case "MC":
		case "CH3CCl3":
			url += "solvents/CH3CCl3/"
			break
		case "CCl4":
			url += "solvents/CCl4/"
			break
		case "C2Cl4":
			url += "solvents/C2Cl4/"
			break
		case "CH2Cl2":
			url += "solvents/CH2Cl2/"
			break
			
		case "H1211":
		case "H1301":
		case "H2402":
			url += "halons/"
			break
			
		// HCFCs
		case "HCFC22":
			url += "hcfcs/hcfc22/"
			break
		case "HCFC141b":
			url += "hcfcs/hcfc141b/"
			break
		case "HCFC142b":
			url += "hcfcs/hcfc142b/"
			break
			
		// HFCs
		case "HFC134A":
		case "HFC152A":
		case "HFC125":
		case "HFC143A":
		case "HFC32":
		case "HFC227ea":
		case "HFC365mfc":
			url += "hfcs/"
			break
			
		// methly halides
		case "CH3Cl":
			url += "methylhalides/ch3cl/"
			break
		case "CH3Br":
			url += "methylhalides/ch3br/"
			break
			
		case "OCS":
		case "COS":
			url += "carbonyl%20sulfide/"
			break
			
		// PERSEUS specific gases
		case "C2H6":
		case "C3H8":
		case "CF4":
		case "HFC236fa":
		case "NF3":
		case "PFC116":
		case "SO2F2":
		case "HFO1234yf":
		case "HFO1234ze":
			url += "PERSEUS/"
			break
						
		default:
			abort "Unrecognized molecule: " + mol
	endswitch

	// program specific path name
	strswitch(prog)
		case "RITS":
			progloc = "insituGCs/RITS/"
			break
		case "CATS":
			progloc = "insituGCs/CATS/"
			break
		case "OldGC":
			progloc = "flasks/OldGC/"
			break
		case "Otto":
			progloc = "flasks/Otto/"
			break
		case "MSD":
			strswitch(mol)
				case "HCFC22":
				case "HCFC142b":
				case "C2Cl4":
				case "CH2Cl2":
				case "h1211":
				case "h1301":
				case "h2402":
				case "CH3Br":
				case "CH3Cl":
					progloc = "flasks/"
					break
				case "F11":
				case "F12":
				case "F113":
				case "CH3CCl3":
					progloc = "flasks/GCMS/"
					break
				default:
					progloc = ""
			endswitch
			break
		case "combined":
			progloc = "combined/"
			break
		default:
			abort "Unrecognized program name"
	endswitch
	
	url += progloc

	// insitu data needs frequency ... otto too
	if ((cmpstr(prog, "RITS")==0) || (cmpstr(prog, "CATS")==0) || (cmpstr(prog, "OTTO")==0))
		url += freq + "/"
	endif
	
	Print "Loading " + mol + " from: " + baseurl + url
	return baseurl + url
	
end


// makes an igor time wave 
function /S TimeWave(prog, mol, freq, site)
	string prog, freq, mol, site
	
	String Tstr
	site = UpperStr(site)
	
	strswitch(freq)
		case "monthly":
			Wave YYYY = $mol + prog + site + "yr" 
			Wave MM = $mol + prog + site + "mon"
			Tstr = mol + LowerStr(prog) + site + "_timeM"
			Make /o/d/n=(numpnts(YYYY))  $Tstr/WAVE=T
			T = date2secs(YYYY, MM, 15)					// roughly the center of the month
			break
		case "daily":
			Wave YYYY = $mol + prog + site + "yr" 
			Wave MM = $mol + prog + site + "mon"
			Wave DD = $mol + prog + site + "day"
			Tstr = mol + LowerStr(prog) + site + "_timeD"
			Make /o/d/n=(numpnts(YYYY))  $Tstr/WAVE=T
			T = date2secs(YYYY, MM, DD) + 12*60*60		// center of day
			break
		case "hourly":
			Wave YYYY = $mol + prog + site + "yr" 
			Wave MM = $mol + prog + site + "mon"
			Wave DD = $mol + prog + site + "day"
			Wave HH = $mol + prog + site + "hour"
			Tstr = mol + LowerStr(prog) + site + "_timeH"
			Make /o/d/n=(numpnts(YYYY))  $Tstr/WAVE=T
			T = date2secs(YYYY, MM, DD) + HH*60*60
			break
	endswitch		
	
	SetScale d 0,0,"dat", T
	return Tstr
end

// the url should point to a ftp directory.  a list of files in the direcotry is returned
// changed Loadwave call to use the /B option (GSD 150213)
function /S ReturnFilesInFTPfolder(url)
	String url

	String response = FetchURL(url)
	
	if (strlen(response) == 0)
		return "No files in " + url
		return ""
	endif

	PutScrapText response
	Loadwave/J/A/B="C=8,N='_skip_';C=1,F=-2,N=tmpfiles;"/V={"\t, "," $",0,0} "Clipboard"
	
	wave /t files = tmpfiles
	String filelst = "", file
	Variable i
	
	for(i=0; i<numpnts(files); i+=1)
		file = files[i]
		if (strlen(file) > 2)
			filelst += files[i] + ";"
		endif
	endfor

	// cleanup
	Killwaves files
	bat("Killwaves /Z @", "wave*")
		
	return filelst
end

Function QuickFigure(m, t, site, mol, sub, prog)
	wave m, t
	string site, mol, sub, prog

	string win = prog + "_" + mol + "_" + site + "_" + sub
	DoWindow /K $win
	Display /K=1 m vs T
	DoWindow /C $win
	
	SetAxis/A/N=1 left
	SetAxis/A/N=1 bottom
	
	Label left prog + " " + UpperStr(site) + " " + mol
	Label bottom "Date"
	
end


