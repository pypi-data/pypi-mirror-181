import os

def make_search_table(log_file, path):

    template ='''<?php
    
function spliteventlog($better_row){
  $res = trim(preg_replace('/\s+/', ' ',$better_row));
  $pieces = explode(" ",$res);
  $num = count($pieces);
  return $pieces;
}''' + '\n\n$arr = file("{}");'.format(log_file) +'''\nforeach($arr as $e){
  $lines[] = preg_replace('!\s!', ',', $e);
}

echo <<<HEAD
<table id="eventtable" style="height: 138px; width: 90%; border-collapse: collapse; margin-left:auto; margin-right:auto;border-style: none;">
<thead>
  <tr style="border-bottom: 3px solid grey; height: 40px; background-color: #ececec;">
    <th style="text-align: center;">Event ID</th>
    <th style="text-align: center;"><h4><strong style="font-size:16px">Class Score</strong><br/> Alerts with score closer to 1 are <br/>more likely to be astrophysical in origin</h4></th>
    <th style="text-align: center;">False Alarm Rate</th>
    <th style="text-align: center;">False Negative Rate</th>
    <th style="text-align: center;">Annotation Time (UTC)</th>
    <th style="text-align: center;">FITS</th>
  </tr>
  <tbody id="eventtablebody">
HEAD;
$data = array_map("str_getcsv", $lines);
foreach($data as $row) {
  $i=0;
  echo "<tr style=\\\"border-bottom: 0.1px solid grey; height: 33px;\\\">\\n";
  $better_row = join(" ",$row);
  $split = spliteventlog($better_row);
  foreach ($split as $e) {
     if ($e == "") continue;
     
     if ($i == 5 | $i==7) {
        $i++;
        continue;
     }
    
     if ($i == 0){
        echo "<td style=\\\"width: 16.5%; height: 24px; text-align: center;\\\"><a href=$split[7]>",$e,"</td>";
        $i++;
     }
     elseif ($i==4) {
        echo "<td style=\\\"width: 16.5%; height: 24px; text-align: center;\\\">",$e, ' ' ,$split[5],"</td>";
        $i++;
     } else
     {
        echo "<td style=\\\"width: 16.5%; height: 24px; text-align: center;\\\">",$e,"</td>";
        $i++;
     }
  }
  echo "</tr>\\n";
}
echo "</tbody>\\n";
echo "</thead>\\n";
echo "</table>\\n";
?>'''
    page = open(path, 'w')
    page.write(template)
    page.close()

    page = open(os.path.join(os.path.dirname(path), '.htaccess'), 'w')
    page.write('AddType application/x-httpd-php .html')
    page.close()


def get_mon_eng(month_num):

    month_to_eng = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'}
    
    return month_to_eng[month_num]
    

def make_summary_template(yr, month, day, path):
    
    yr_str    = '{:04d}'.format(yr)
    month_str = '{:02d}'.format(month)
    day_str   = '{:02d}'.format(day)
    
    month_eng = get_mon_eng(month_str)
    
    template = '''<!DOCTYPE HTML>
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta content="width=device-width, initial-scale=1.0" name="viewport" />
<base href="../../" />
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/fontawesome.min.css" rel="stylesheet" media="all" />
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/solid.min.css" rel="stylesheet" media="all" />
<link href="https://cdn.jsdelivr.net/npm/gwbootstrap@1.3.1/lib/gwbootstrap.min.css" rel="stylesheet" media="all" />
<script src="https://code.jquery.com/jquery-3.5.1.min.js" type="text/javascript"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js" type="text/javascript"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js" type="text/javascript"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" type="text/javascript"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/fancybox/3.5.7/jquery.fancybox.min.js" type="text/javascript"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js" type="text/javascript"></script>
<script src="https://cdn.jsdelivr.net/npm/gwbootstrap@1.3.1/lib/gwbootstrap-extra.min.js" type="text/javascript"></script>

<style>
h1{font-family:"HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;font-weight:300;font-size:35px;}
body {background-color: #EEEEEE; font-family:"HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;font-weight:300;font-size:14px;}
p{font-family:"HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;font-size:15px;}
p.emptyline {border-bottom: solid 5px #CDCDCD;}
</style>

''' + '''\n<title> GWSkyNet Summary %s-%s-%s </title>'''%(day_str, month_str, yr_str) + '''\n<h1 style="margin-left:38px;margin-top:65px"> GWSkyNet Summary %s %s %s </h1>'''%(month_eng, day_str, yr_str) + '''\n<p class="headertxt" style ="margin-left:40px"> Events released on graceDB that have been annotated on %s %s %s by GWSkyNet can be found here. </p>'''%(month_eng, day_str, yr_str)+ '''\n<input style="margin-left:38px; font-size:12px" type="text" id="searchbarinput" onkeyup="eventsearchbar()" placeholder="&nbsp;&nbsp;Search for Events"/>
<p class="emptyline"> </p>
</head>
<body>
  

<button title="Return to top" class="btn-float shadow" id="top-btn"><i class="fas fa-arrow-up"></i></button>
<nav class="navbar fixed-top navbar-expand-md shadow-sm">
<div class="container-fluid">

<ul class="nav navbar-nav mr-auto">
<li class="nav-item">
<a class="nav-link step-back" title="Step backward">&laquo;</a>
</li>
<li class="nav-item">'''+'''\n<a id="calendar" class="nav-link dropdown-toggle" title="Show/hide calendar"  data-date="%s-%s-%s" data-date-format="dd-mm-yyyy" data-viewmode="days" background-color:"#FF0000">%s-%s-%s</a>'''%(day_str, month_str, yr_str, day_str, month_str, yr_str) + '''\n</li>
<li class="nav-item">
<a class="nav-link step-forward" title="Step forward">&raquo;</a>
</li>
</ul>
<div>
</nav>

<style>
      h4 {

        font-size: 10px;
      }

      h4:first-line {
        font-size: 16px;
        font-weight: bold;
      }

    </style>
<?php
   include("search.php");
?>
<script>
      function eventsearchbar() {
        // Declare variables
        var input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("searchbarinput");
        filter = input.value.toUpperCase();
        table = document.getElementById("eventtable");
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows, and hide those who don't match the search query
        for (i = 0; i < tr.length; i++) {
          td = tr[i].getElementsByTagName("td")[0];
          if (td) {
            txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
          } else {
          tr[i].style.display = "none";
          }
          }
          }
       }
</script>
</body>
</html>'''
    page = open(path, 'w')
    page.write(template)
    page.close()

