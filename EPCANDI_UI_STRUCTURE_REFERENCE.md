# EPC&I Website - UI Structure & Layout Reference

## Overview
The EPC&I website uses a classic ASP.NET layout with a fixed-width design (984-1004px). All pages share the same navigation structure, left panel layout, and consistent CSS styling.

---

## 1. OVERALL PAGE LAYOUT STRUCTURE

### Main Container Classes:
```html
<div id="main" class="main-div">
    <!-- Logo & Top Bar -->
    <div id="topbar" class="topbar-div">
        <a href="index.html">
            <img alt="logo" src="./epcandi_files/logo.png" class="tb_logo">
        </a>
    </div>
    
    <!-- Navigation Menu Bar -->
    <div id="menubar" class="menu-div">
        <!-- Menu items with pipes separator -->
    </div>
    
    <!-- Main Content Wrapper -->
    <div id="contentwrapper" class="contentwrapper-div">
        <table border="0" cellpadding="0" cellspacing="0" width="984px">
            <tr>
                <!-- Left Panel -->
                <td valign="top">
                    <div id="leftpanel" class="leftpanel-div"></div>
                </td>
                
                <!-- Center Content -->
                <td valign="top">
                    <div id="content" class="content-div"></div>
                </td>
                
                <!-- Right Panel (sometimes present) -->
                <td valign="top">
                    <div id="rightpanel"></div>
                </td>
            </tr>
        </table>
    </div>
</div>
```

### CSS Classes for Layout:
```css
.main-div {
    width: 1004px;
    margin: 0px;
    padding: 0px;
    background: url(/images/rs_bg.gif) repeat;
}

.topbar-div {
    width: 984px;
    height: 94px;
    background: url(/images/scanlines.gif) no-repeat center top;
}

.menu-div {
    width: 984px;
    height: 26px;
    background: url(/images/menubarbg1.jpg) repeat center top;
}

.contentwrapper-div {
    width: 984px;
    border-bottom: solid 1px #c9252b;
}

.leftpanel-div {
    width: 200px;
}

.content-div {
    width: 564px;
    text-align: center;
    vertical-align: top;
}
```

---

## 2. NAVIGATION MENU STRUCTURE

### Menu Bar HTML:
```html
<div id="menubar" class="menu-div">
    <!-- NEWS (with submenu) -->
    <a href="..." class="anchorclass" rel="newsmenu">
        <img alt="NEWS" src="./epcandi_files/m_news_glow.gif" 
             height="20" width="42" onmouseover="document.news.src='./epcandi_files/m_news_oglow.gif'" 
             onmouseout="document.news.src='./epcandi_files/m_news_glow.gif'">
    </a>
    <img alt="pipe" src="./epcandi_files/m_pipe.gif" class="menu-pipe">
    
    <!-- ARTICLES -->
    <a href="EPC&I ARTICLES.html">
        <img alt="ARTICLES" src="./epcandi_files/m_articles_glow.gif" 
             height="20" width="68">
    </a>
    <img alt="pipe" src="./epcandi_files/m_pipe.gif" class="menu-pipe">
    
    <!-- INTERVIEWS -->
    <a href="EPC&I INTERVIEWS.html">
        <img alt="INTERVIEWS" src="./epcandi_files/m_interviews_glow.gif" 
             height="20" width="83">
    </a>
    <img alt="pipe" src="./epcandi_files/m_pipe.gif" class="menu-pipe">
    
    <!-- EQUIPMENT NEWS -->
    <a href="EPC&I EQUIPMENT NEWS.html">
        <img alt="EQUIPMENT NEWS" src="./epcandi_files/m_equipmentnews_glow.gif" 
             height="20" width="121">
    </a>
    <img alt="pipe" src="./epcandi_files/m_pipe.gif" class="menu-pipe">
    
    <!-- TENDERS (with submenu) -->
    <a href="..." class="anchorclass" rel="tendersmenu">
        <img alt="TENDERS" src="./epcandi_files/m_tenders_glow.gif" 
             height="20" width="65">
    </a>
    <img alt="pipe" src="./epcandi_files/m_pipe.gif" class="menu-pipe">
    
    <!-- EVENTS -->
    <a href="EPC&I EVENTS.html">
        <img alt="EVENTS" src="./epcandi_files/m_events_glow.gif" 
             height="20" width="54">
    </a>
    <img alt="pipe" src="./epcandi_files/m_pipe.gif" class="menu-pipe">
    
    <!-- CATALOGS -->
    <a href="...">
        <img alt="CATALOGS" src="./epcandi_files/m_catalogs_glow.gif" 
             height="20" width="75">
    </a>
    <img alt="pipe" src="./epcandi_files/m_pipe.gif" class="menu-pipe">
    
    <!-- SUBSCRIBE -->
    <a href="EPC&I USER REGISTRATION subscribe.html">
        <img alt="SUBSCRIBE" src="./epcandi_files/m_subscribe_glow.gif" 
             height="20" width="78">
    </a>
    <img alt="pipe" src="./epcandi_files/m_pipe.gif" class="menu-pipe">
    
    <!-- CONTACT US -->
    <a href="CONTACT EPC&I.html">
        <img alt="CONTACT US" src="./epcandi_files/m_contactus_glow.gif" 
             height="20" width="86">
    </a>
</div>
```

### Menu CSS:
```css
.menu-div {
    background: url(/images/menubarbg1.jpg) repeat center top;
    width: 984px;
    height: 26px;
    text-align: left;
    vertical-align: middle;
}

.menu-pipe {
    margin: 3px 12px 3px 12px;
}
```

---

## 3. LEFT PANEL STRUCTURE

### Latest Issue Section:
```html
<div id="leftpanel" class="leftpanel-div">
    <!-- Latest Issue Box -->
    <div id="latestissue" class="lp_issue">
        <a href="contents.aspx?issueid=460138">
            LATEST ISSUE - DECEMBER 2025- EXCON
            <br class="zerospacer">
            <img alt="DECEMBER 2025- EXCON" src="./epcandi_files/issue_460138.jpg">
        </a>
    </div>
    
    <!-- Optional: Featured Catalogs (commented out in current version) -->
    <!-- 
    <div id="featuredcatalogs" class="lp_catalog">
        <img alt="FEATURED CATALOGS" src="./epcandi_files/featuredcatalog.gif" />
        <img alt="" src="./epcandi_files/bullet1.gif" class="lp_catalog_bullet" />Pidilite Industries Ltd.
        ...
    </div>
    -->
</div>
```

### Left Panel CSS:
```css
.leftpanel-div {
    width: 200px;
}

.lp_issue {
    margin-left: 10px;
    margin-top: 12px;
    text-align: left;
}

.lp_catalog {
    width: 191px;
    font-size: 10px;
    margin-top: 12px;
    margin-left: 5px;
    line-height: 18px;
    border-style: inset;
    border-width: 1px;
    border-color: #a7a9ac;
}

.lp_catalog_bullet {
    margin: 3px 5px 0px 8px;
}

.banner {
    margin-top: 12px;
    text-align: center;
}

.zerospacer {
    clear: both;
    margin: 0px;
}
```

---

## 4. EVENTS PAGE STRUCTURE

### Full Events Page Layout:
```html
<div id="latestarticle" style="width:512px; margin:21px 26px 0px 26px; text-align:left;">
    
    <!-- Header -->
    <div id="titleimage" style="background:none; width:512px; height:32px; font-size:11px; text-align:right; vertical-align:middle;">
        EVENTS PER PAGE:&nbsp;
        <select name="dd_pageSize" id="dd_pageSize" class="articles-per-page">
            <option value="2">2</option>
            <option value="10">10</option>
            <option selected="selected" value="20">20</option>
            <option value="50">50</option>
        </select>
    </div>
    
    <!-- Filter Section -->
    <div id="filters" class="list-article-filters">
        <input name="txtShowpage" type="hidden" id="txtShowpage">        
        FILTER YOUR RESULTS:&nbsp;<br><br>
        &nbsp;EVENT NAME:&nbsp;
        <input name="txt_event_name" type="text" id="txt_event_name">
        <span style="font-size:9px;">&nbsp;&nbsp;AND/OR&nbsp;&nbsp;</span>
        EVENT DATE:&nbsp;
        <input name="txt_date" type="text" id="txt_date" class="form-text">        
        &nbsp;&nbsp;
        <input type="image" name="but_filter" id="but_filter" src="./epcandi_files/but_apply.gif" align="middle">
    </div>
    
    <!-- Pagination Top -->
    <div id="pager_top" class="pager-top">
        <span class="pager-selected">1</span>&nbsp;
    </div>
    
    <!-- Events List Container -->
    <div id="repeater">
        <!-- Each Event Item -->
        <div class="list-event-header">EVENT NAME</div>
        <div class="list-event-details">
            <img alt="" src="./epcandi_files/event_270091.jpg" class="list-event-image">
            <b>29/08/2025  -  31/08/2025</b><br><br>
            <u>Venue</u>: Event Venue Details<br><br>
            <u>Timing</u>: 10:00 am to 6:00 pm<br><br>
            <u>Contact</u>: Contact Person Details<br><br>
            <a href="https://example.com/" target="_blank">https://example.com/</a>
        </div>
        <div id="seperator" class="list-seperator">*****</div>
        
        <!-- More events follow same pattern -->
    </div>
    
    <!-- Pagination Bottom -->
    <div id="pager_bottom" class="pager-bottom">
        <span class="pager-selected">1</span>&nbsp;
    </div>
</div>
```

### Events Page CSS:
```css
.list-event-header {
    background: url(/images/mbbullet2.gif) no-repeat 0px 7px;
    margin: 15px 0px 0px 12px;
    padding: 0px 0px 0px 12px;
    font-size: 14px;
    vertical-align: bottom;
    clear: both;
}

.list-event-details {
    text-align: left;
    font-size: 11px;
    margin: 7px 0px 0px 12px;
    padding: 0px 0px 0px 12px;
    clear: both;
}

.list-event-image {
    float: right;
    margin: 4px 4px 4px 4px;
}

.list-seperator {
    margin: 15px 0px 0px 12px;
    color: #000000;
    font-size: 10px;
    font-weight: bold;
    text-align: center;
    vertical-align: middle;
    float: none;
    clear: both;
}

.list-article-filters {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 11px;
    padding: 10px 5px 0px 5px;
    text-align: left;
    vertical-align: middle;
}

.articles-per-page {
    font-family: Verdana, Arial, Helvetica, Sans-Serif;
    font-size: 11px;
    margin: 9px 10px 9px 0px;
}

.pager-top {
    width: 100%;
    font-size: 10px;
    text-align: center;
    vertical-align: bottom;
    margin: 10px 0px 20px 0px;
    border: solid 1px #58595b;
}

.pager-bottom {
    width: 100%;
    font-size: 10px;
    text-align: center;
    vertical-align: top;
    margin: 20px 0px 20px 0px;
    border: solid 1px #58595b;
}

.pager-selected {
    font-size: 10px;
    font-weight: bold;
    color: #000000;
}
```

---

## 5. CONTACT FORM PAGE STRUCTURE

### Contact Form HTML:
```html
<div id="latestarticle" style="width:512px; margin:21px 26px 0px 26px; text-align:left;">
    <img alt="USER REGISTRATION" src="./epcandi_files/headerregistration.gif">
    
    <div id="rates" style="text-align:center; margin:15px 0px 15px 0px;">
        <b>Please fill in the form below and we will get back to you ASAP.</b><br>
        <span id="err_label"></span>
    </div>
    
    <div id="subscriptionform" class="form-content">
        <!-- Left Column: Labels -->
        <div style="float:left; width:240px; margin:0px 0px 0px 0px;">
            <p style="height:25px; vertical-align:middle;">Nature Of Query:</p>
            <p style="height:25px; vertical-align:middle;">Your Name:</p>
            <p style="height:25px; vertical-align:middle;">Email:&nbsp;</p>
            <p style="height:25px; vertical-align:middle;">Organisation:</p>
            <p style="height:25px; vertical-align:middle;">Subject:</p>
            <p style="height:65px; vertical-align:middle;">Message:</p>
        </div>
        
        <!-- Right Column: Input Fields -->
        <div style="margin:0px 0px 0px 0px;">
            <p style="height:25px; vertical-align:middle;">
                <select name="dd_query" id="dd_query" class="form-text">
                    <option selected="selected" value="Feedback / Suggestions">Feedback / Suggestions</option>
                    <option value="Sales">Sales</option>
                    <option value="Customer Care">Customer Care</option>
                </select>
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_name" type="text" maxlength="250" id="txt_name" class="form-text">
                <span>&nbsp;&nbsp;&nbsp;</span>&nbsp;
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_email" type="text" maxlength="256" id="txt_email" class="form-text">
                <span>&nbsp;&nbsp;&nbsp;</span>&nbsp;
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_organisation" type="text" maxlength="100" id="txt_organisation" class="form-text">
                <span>&nbsp;&nbsp;&nbsp;</span>
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_subject" type="text" maxlength="250" id="txt_subject" class="form-text">
                <span>&nbsp;&nbsp;&nbsp;</span>&nbsp;
            </p>
            <p style="height:65px; vertical-align:middle;">
                <textarea name="txt_message" rows="2" cols="20" id="txt_message" class="form-text"></textarea>
                <span>&nbsp;&nbsp;&nbsp;</span>&nbsp;
            </p>
        </div>
        
        <!-- CAPTCHA Verification -->
        <div style="text-align:center; margin:15px 0px 15px 0px; width:512px; float:none; clear:both;">
            <img id="Image1" src="./epcandi_files/imgbuynenfrawa3b3vazjdnhfdd.gif">
        </div>
        
        <div style="text-align:center; margin:15px 0px 15px 0px;">
            Please enter the characters in the image above for verification.<br>
            <input name="txt_verification" type="text" id="txt_verification">
            &nbsp;
        </div>
        
        <!-- Submit Button -->
        <div style="text-align:center; height:25px; margin:15px 0px 15px 0px;">
            <input type="image" name="ImageButton1" id="ImageButton1" src="./epcandi_files/but_submit.gif">
        </div>
    </div>
</div>
```

### Contact Form CSS:
```css
.form-content {
    margin: 15px 0px 0px 0px;
    width: 500px;
    font-size: 11px;
    text-align: left;
    vertical-align: top;
    clear: both;
}

.form-text {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 11px;
}

.form-content p {
    height: 25px;
    vertical-align: middle;
}
```

---

## 6. SUBSCRIBE/REGISTRATION FORM PAGE STRUCTURE

### Registration Form HTML:
```html
<div id="latestarticle" style="width:512px; margin:21px 26px 0px 26px; text-align:left;">
    <img alt="USER REGISTRATION" src="./epcandi_files/headerregistration.gif">
    
    <div id="rates" style="text-align:center; margin:15px 0px 15px 0px;">
        <b>Register Now for a free copy of EPC&I.</b><sup>*CONDITIONS APPLY.</sup><br>
        <span id="err_label"></span>
    </div>
    
    <div id="subscriptionform" class="form-content">
        <!-- Left Column: Labels -->
        <div style="float:left; width:240px; margin:0px 0px 0px 0px;">
            <p style="height:25px; vertical-align:middle;">First Name:</p>
            <p style="height:25px; vertical-align:middle;">Last Name:</p>
            <p style="height:25px; vertical-align:middle;">Designation:</p>
            <p style="height:25px; vertical-align:middle;">Organisation:</p>
            <p style="height:45px; vertical-align:middle;">Address:</p>
            <p style="height:25px; vertical-align:middle;">City:</p>
            <p style="height:25px; vertical-align:middle;">State:</p>
            <p style="height:25px; vertical-align:middle;">Pincode:</p>
            <p style="height:25px; vertical-align:middle;">Telephone No.:</p>
            <p style="height:25px; vertical-align:middle;">Mobile:</p>
            <p style="height:25px; vertical-align:middle;">Email:</p>
            <p style="height:25px; vertical-align:middle;">Password:</p>
            <p style="height:25px; vertical-align:middle;">Confirm Password:</p>
        </div>
        
        <!-- Right Column: Input Fields -->
        <div style="margin:0px 0px 0px 0px;">
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_fname" type="text" maxlength="50" id="txt_fname" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_lname" type="text" maxlength="100" id="txt_lname" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_designation" type="text" maxlength="50" id="txt_designation" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_organisation" type="text" maxlength="100" id="txt_organisation" class="form-text">
            </p>
            <p style="height:45px; vertical-align:middle;">
                <textarea name="txt_address" rows="2" cols="20" id="txt_address" class="form-text"></textarea>
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_city" type="text" maxlength="50" id="txt_city" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_state" type="text" maxlength="50" id="txt_state" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_pincode" type="text" maxlength="10" id="txt_pincode" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_phone" type="text" maxlength="50" id="txt_phone" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_mobile" type="text" maxlength="50" id="txt_mobile" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_email" type="text" maxlength="256" id="txt_email" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_Password" type="password" maxlength="50" id="txt_Password" class="form-text">
            </p>
            <p style="height:25px; vertical-align:middle;">
                <input name="txt_confirmpassword" type="password" maxlength="50" id="txt_confirmpassword" class="form-text">
            </p>
        </div>
        
        <!-- Pricing Table -->
        <div style="text-align:center; margin:15px 0px 15px 0px; width:512px; float:none; clear:both;">
            <table border="1" cellpadding="2" cellspacing="1" width="512">
                <tr>
                    <td align="center"><b>PERIOD</b></td>
                    <td align="center"><b>STAND PRICE</b></td>
                    <td align="center" style="color:#c9252b; background-color:#d1d3d4;"><b>YOU PAY</b></td>
                    <td align="center"><b>SAVE</b></td>
                </tr>
                <tr>
                    <td align="left" style="padding:0px 0px 0px 15px;">1 Year (12 Issues)</td>
                    <td align="left" style="padding:0px 0px 0px 15px;">Rs. 720.00</td>
                    <td align="left" style="padding:0px 0px 0px 15px; color:#c9252b; background-color:#d1d3d4;">Rs. 600.00</td>
                    <td align="left" style="padding:0px 0px 0px 15px;">Rs. 120.00</td>
                </tr>
                <!-- More pricing rows -->
            </table>
        </div>
    </div>
</div>
```

### Registration Form Key Fields:
- First Name (max 50 chars)
- Last Name (max 100 chars)
- Designation (max 50 chars)
- Organisation (max 100 chars)
- Address (textarea, 2 rows)
- City (max 50 chars)
- State (max 50 chars)
- Pincode (max 10 chars)
- Telephone No. (max 50 chars)
- Mobile (max 50 chars)
- Email (max 256 chars)
- Password (max 50 chars)
- Confirm Password (max 50 chars)

---

## 7. KEY CSS STYLING REFERENCE

### General Typography:
```css
body {
    margin: 0px;
    font-family: Verdana, Arial, Helvetica, sans-serif;
    color: #58595b;
    font-size: 12px;
}

a {
    text-decoration: none;
    color: inherit;
}

img {
    border-width: 0px;
}
```

### Input Form Elements:
```css
.form-text {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 11px;
}

input[type="text"],
textarea,
select {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 11px;
}
```

### Error Messages:
```css
.err-msg {
    font-size: 11px;
    text-decoration: underline;
    color: #c9252b;
}
```

### Instruction Text:
```css
.instruction {
    font-size: 11px;
    font-family: Arial, Verdana;
    color: #414042;
}
```

---

## 8. COLOR SCHEME

- **Primary Red**: `#c9252b` (used for accents, highlights, errors)
- **Dark Text**: `#58595b` (main body text)
- **Light Border**: `#a7a9ac` (form borders, panel edges)
- **Black**: `#000000` (headers, bold text)
- **Light Gray**: `#d1d3d4` (table backgrounds, highlights)
- **Dark Gray**: `#414042` (instruction text)

---

## 9. COMMON PATTERNS ACROSS ALL PAGES

### Hidden Form Fields (ASP.NET):
```html
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="...">
<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="...">
<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="...">
```

### Generic Page Structure:
1. DOCTYPE XHTML 1.0 Transitional
2. Meta charset UTF-8
3. External CSS in: `./[PageName]_files/style.css`
4. External CSS for menu: `./[PageName]_files/anylinkcssmenu.css`
5. Google Analytics script included
6. Form wrapper: `<center><form method="post" action="[PageName].html" id="form1">`

### Consistent Elements on Every Page:
- Logo in top-left (class: `tb_logo`)
- Image-based navigation menu (height: 26px)
- Left sidebar with "Latest Issue" box
- Central content area (width: 512px)
- Optional right sidebar for advertisements

---

## 10. FORM INPUT STYLING PATTERNS

### Text Input Pattern:
```html
<p style="height:25px; vertical-align:middle;">
    <input name="field_name" type="text" maxlength="XX" id="field_name" class="form-text">
    <span>&nbsp;&nbsp;&nbsp;</span>
</p>
```

### Textarea Pattern:
```html
<p style="height:45px; vertical-align:middle;">
    <textarea name="field_name" rows="2" cols="20" id="field_name" class="form-text"></textarea>
    <span>&nbsp;&nbsp;&nbsp;</span>
</p>
```

### Dropdown/Select Pattern:
```html
<p style="height:25px; vertical-align:middle;">
    <select name="dd_fieldname" id="dd_fieldname" class="form-text">
        <option selected="selected" value="option1">Option 1</option>
        <option value="option2">Option 2</option>
    </select>
</p>
```

### Image Button Pattern:
```html
<input type="image" name="button_name" id="button_name" src="./epcandi_files/but_[buttontype].gif">
```

---

## 11. LAYOUT DIMENSIONS

- **Main Container**: 1004px wide
- **Content Wrapper**: 984px wide
- **Left Panel**: 200px wide
- **Center Content**: 564px wide
- **Right Panel**: Remaining width (usually for ads)
- **Form Content**: 500-512px wide
- **Max Input Width**: Typically 90% of container
- **Image Event Thumbnails**: ~150px width (floated right)
- **Top Bar Height**: 94px
- **Menu Bar Height**: 26px

---

## 12. JAVASCRIPT BEHAVIORS

- **Pagination Function**: `pager(n)` - Changes page by updating hidden txtShowpage field and submitting form
- **Menu Hover Effects**: Inline onmouseover/onmouseout handlers change image sources
- **AnyLink CSS Menu**: Uses `anylinkcssmenu.js` for dropdown menus on NEWS and TENDERS
