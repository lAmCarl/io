%import operator

<html>
<head>
<style>
	th, td {
		padding: 10px;
	}
</style>
</head>
<body>

<img src="cow.jpg">
<img src="name.png">

<form action="/" method="get"> Search: <input name="keywords" type="text" /> 
      <input value="Submit" type="submit" /> </form>

<%
if history:
  ord_history = sorted(history.items(), key=lambda x: x[1])
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
% end
</body>
</html>