//const vueApp =

new Vue({                   // controls whole or certain part of application - search part
    el: "#vue-app",         // Connects to the DOM
    data: {                 // Different key value pairs in the data object
          mentors: [],
          search:"",
          name:'Rupal',
          searchProps:["location", "name", "description"],
    },

    delimiters: ['[[',']]'],

    methods: {

    },
    // Only called once at the beginning
    created(){
       //    https://vue-project-net-ninja.firebaseio.com/posts.json
       //    https://women-mentoring.firebaseio.com/.json
       this.$http.get('https://women-mentoring.firebaseio.com/.json').then(function(data){
           // this.mentors = data.body.slice(0,10); // gets first 10 elements
           // we are getting array from here and storing in the blogs property above
           return data.json() //data.json() is asynchronous task - takes some time to complete
       }).then(function(data){
      var mentorsArray = [];
      for (let key in data){
        // key refers to the unique id in the database;
        // data is the parent object which inlcudes the child objects each one being a different blog post
        data[key].id = key;
        mentorsArray.push(data[key]);
      }
      this.mentors = mentorsArray;
        });
    },

// WORKING JUST FINE:
//    computed:{
//    filteredMentors: function(){
//      return this.mentors.filter((mentor) => {
////        console.log(mentor.name.match('a'))
////        console.log(mentor.name.match(this.search))
////        return mentor.name.toUpperCase().match(this.search.toUpperCase());
//        var upSearch = this.search.toUpperCase()
//        return this.searchProps.some( key =>
//        String(mentor[key]).toUpperCase().includes(upSearch) );
////        return keys.some( key =>
////            String(mentor[key]).toUpperCase().includes(upSearch)
//            });
//        }
//    },

    computed:{
        filteredMentors: function(){
          return this.mentors.filter((mentor) => {
            var upSearch = this.search.toUpperCase()
            return this.searchProps.some( key =>
            String(mentor[key]).toUpperCase().includes(upSearch);
            console.log(String(mentor[key]).toUpperCase().includes(upSearch));
            );
//            .replace(upSearch, '<span class="highlight">' + query + '</span>')
                });
            }
        }

});
