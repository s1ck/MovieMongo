function format_result(result){
  img_url = result.img_url ? result.img_url : "http://placehold.it/250x150";
  url = result._id.$oid;//source+"?id="+result.id;
  
  if (result.my_movie === true)
    status = "<a href='#' id='del_movie' title='Remove movie from collection' onclick=\"return del_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check del'></i>"
    + "</a>";
  else
    status = "<a href='#' id='add_movie' title='Add movie to collection' onclick=\"return add_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check add'></i>"
    + "</a>";
  
  return "<li class='media thumbnail'>"
    + "<div class='media-body'>"
    + "  <a class='pull-left' href='/"+url+"'>"
    + "    <img class='media-object' data-src='holder.js/250x150' />"
    + "    <img class='media-object result' src='" + img_url + "' /> "
    + "  </a>"
    + "  <a href='/"+url+"'><h3 id='name' class='media-heading'>"+result.name+"</h3></a>&nbsp;"
    + status
    + "  <p>Source: " + result.source + "</p>"
    + "</div>"
    + "</li>";
}

function format_details(result){
  img_url = result.img_url ? result.img_url : "http://placehold.it/250x150";
  if (result.my_movie)
    status = "<a href='#' id='del_movie' title='Remove movie from collection' onclick=\"return del_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check del'></i>"
    + "</a>";
  else
    status = "<a href='#' id='add_movie' title='Add movie to collection' onclick=\"return add_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check add'></i>"
    + "</a>";
  
  out = "<div class='media-body thumbnail' style='padding:10px'>"
    + "  <img class='media-object result pull-left' style='margin-right:10px' src='" + img_url + "' /> "
    + "  <h3 id='name' class='media-heading'>"+result.name+"</h3> "
    + status
    + "<p><strong>Source:</strong> " + result.source + "</p>"

    + "  <hr/><div class='pull-left'><h4>Details:</h4><dl class='dl-horizontal'>";
  out += result.actors.length > 0 ? "<dt>actors:</dt><dd><ul><li>" + result.actors.join("</li><li>") + "</li></ul></dd>" : "";
  out += result.directed_by.length > 0 ? "<dt>directed_by:</dt><dd><ul><li>" + result.directed_by.join("</li><li>") + "</li></ul></dd>" : "";
  out += result.genre.length > 0 ? "<dt>genre:</dt><dd><ul><li>" + result.genre.join("</li><li>") + "</li></ul></dd>" : "";
  out += result.initial_release_date ? "  <dt>released:</dt><dd>" + result.initial_release_date + "</dd>" : "";
  out += result.written_by.length > 0 ? "<dt>written by:</dt><dd><ul><li>" + result.written_by.join("</li><li>") + "</li></ul></dd>" : "";
  out += "</dl></div>";
  if (result.my_movie){
    out += "<div class='pull-right' style='width:40%'><h4>User content:</h4><div id='forms' class='pull-right'>";
    out += "<table><tr><td><strong>verborgt an:</strong></td><td>Andreas</td><td><i class='icon-minus-sign'></i></td></tr>";
    out += "<tr><td><input type='text' class='input-small' placeholder='Key'/></td><td><input type='text' placeholder='Value'/></td><td><i class='icon-plus-sign'></i></td></tr></table>";
    out += "</div></div>";
  }
  out += "</div>";
  return out;
}

function add_movie(event, id){
  console.log(event);
  event.preventDefault();
  $.ajax({
    url: "http://localhost:8080/",
    type: "POST",
    data: {id: id},
    success: function(data){
      $("#add_movie").remove();
      $("#name").after(" <a href='#' id='del_movie' title='Remove movie from collection' onclick=\"return del_movie(event,\'"+id+"\')\">"
				   +   "<i class='icon-check del'></i>"
				   + "</a>");
      
      console.log("success");
    }
  });
  //return false;
}

function del_movie(event, id){
  console.log(event);
  event.preventDefault();
  $.ajax({
    url: "http://localhost:8080/",
    type: "DELETE",
    data: {id: id},
    success: function(data){
      $("#del_movie").remove();
      $("#name").after(" <a href='#' id='add_movie' title='Add movie to collection' onclick=\"return add_movie(event,\'"+id+"\')\">"
				   +   "<i class='icon-check add'></i>"
				   + "</a>");

      console.log("success");
    }
  });
  //return false;
}
