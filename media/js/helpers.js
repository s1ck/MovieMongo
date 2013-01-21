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
  //status = result.my_movie === true ? "V" : "<a href='#' id='add_movie' onclick=\"add_movie(\'"+result.source+"\',\'"+result.id+"\')\">Add</a>";
  if (result.my_movie === true)
    status = "<a href='#' id='del_movie' title='Remove movie from collection' onclick=\"return del_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check del'></i>"
    + "</a>";
  else
    status = "<a href='#' id='add_movie' title='Add movie to collection' onclick=\"return add_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check add'></i>"
    + "</a>";
  
  out = "<div class='media-body thumbnail'>"
    + "  <a class='pull-left' href='/"+result.source+"?id="+result.id+"'>"
    + "    <img class='media-object result' src='" + img_url + "' /> "
    + "  </a>"
    + "  <h3 id='name' class='media-heading'>"+result.name+"</h3> "
    + status
    + "  <dl class='dl-horizontal' style='margin-top:50px'>"
    + "  <dt>Source:</dt><dd>" + result.source + "</dd>";
  out += result.actors.length > 0 ? "<dt>actors:</dt><dd>" + result.actors + "</dd>" : "";
  out += result.directed_by.length > 0 ? "<dt>directed_by:</dt><dd>" + result.directed_by + "</dd>" : "";
  out += result.genre.length > 0 ? "<dt>genre:</dt><dd>" + result.genre + "</dd>" : "";
  out += result.initial_release_date ? "  <dt>released:</dt><dd>" + result.initial_release_date + "</dd>" : "";
  out += result.written_by.length > 0 ? "<dt>written by:</dt><dd>" + result.written_by + "</dd>" : "";
  out += "</dl></div>";
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
