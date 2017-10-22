<html>
<head>
<style>
	th, td {
		padding: 10px;
	}
</style>
</head>
<body>

% if user:
  <h3>{{user}}</h3>
  <form action="/signout">
    <input type="submit" value="Signout"/>
  </form>
% else:
  <form action="/signin">
    <input type="submit" value="Signin"/>
  </form>
% end

<img src="cow.jpg">
<img src="name.png">
<br>
<form action="/">
  <input type="submit" value="Back"/>
</form>
<h3> Results: </h3>

<p> Search for "<i>{{query}}</i>" </p>

<table id="results">
  <tr>
    <th><b>Word</b></th>
    <th><b>Count</b></th>
  </tr>

<%

for word, count in word_count.items():
%>
  <tr>
	<td>{{word}}</td>
    <td>{{count}}</td>
  </tr>
  % end
</table>

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
