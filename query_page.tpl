<html>
<head>
  <link rel="stylesheet" type="text/css" href="/query_style.css">
</head>
<body>

<!-- Sign-in/sign-out button -->
<div class="right">
  % if user:
    <h3>{{user}}</h3>
    <form action="/signout">
      <input type="submit" value="Sign-out"/>
    </form>
  % else:
    <form action="/signin">
      <input type="submit" value="Sign-in"/>
    </form>
  % end
</div>
<!-- Logo and search bar -->
<div class="center">
  <img src="cow.png" alt="Cow Logo" align="middle">
  <img src="name.png" alt="Io" align="middle">

  <form action="/" method="get"> <input name="keywords" type="text" placeholder="Search..."/> 
        <input value="Submit" type="submit" /> </form>
</div>

<!-- Search history, for sign-in only -->
<%
if history and len(history['count']):
  ord_history = sorted(history['count'].items(), key=lambda x: x[1])
  ord_history.reverse()
%>

<h3> Top Twenty Keywords: </h3>
<table id="history">
  <tr>
    <th><b>Word</b></th>
    <th><b>Count</b></th>
  </tr>
<%
  for i in range(min(len(ord_history),20)):
%>
  <tr>
	<td>{{ord_history[i][0]}}</td>
    <td>{{ord_history[i][1]}}</td>
  </tr>
  % end
</table>

<h3> Recent Searches: </h3>
<table id="recents">
  <tr>
    <th><b>Word</b></th>
  </tr>
<% for word in history['recent']:%>
  <tr>
  <td>{{word}}</td>
  </tr>
  % end
</table>
% end
</body>
</html>
