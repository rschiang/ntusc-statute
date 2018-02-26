fetch('https://rschiang.github.io/ntusc-statute/version.json').then(function(response) {
  var version = JSON.parse(response.body);
  var footer = document.querySelector('footer');
  var root = document.createElement('div');
  root.setAttribute('class', 'version-info');
  root.innerHTML = '法規版本 '+
  '<a class="commit" href="https://github.com/ntu-student-congress/tortue/commit/'+version.statute+'">'+version.statute.sub(0,7)+'</a>'+
  '，建置版本 '+
  '<a class="commit" href="https://github.com/rschiang/ntusc-statute/commit/'+version.build+'">'+version.build.sub(0,7)+'</a>'+
  '('+ version.date +')';
  footer.appendChild(root);
})
