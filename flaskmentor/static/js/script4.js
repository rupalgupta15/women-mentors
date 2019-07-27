//const vueApp =

var router = new VueRouter({
    mode: 'history',
    routes: []
});

new Vue({                   // controls whole or certain part of application - search part
    router,
    el: "#vue-app",         // Connects to the DOM
    mounted: function() {
        var queryString = this.$route.query.query;
        if (typeof queryString === 'undefined')
        {
            queryString = " "
        }
        this.search = queryString    // This gets us the query parameter from the url
        // for (let q in this.$route.query){console.log(q)}
//        console.log(this.$route.query.query)

    },
    data: {                 // Different key value pairs in the data object
          mentors: [],
          search:"",
          searchProps:["location", "name", "description"],
          noneObject: null
//          selected: ''
    },

    delimiters: ['[[',']]'],

    methods: {

    },
    // Only called once at the beginning
    created(){
//       console.log(this.selected);
       //    https://women-mentoring.firebaseio.com/.json
       this.$http.get('https://women-mentors.firebaseio.com/.json').then(function(data){
           // this.mentors = data.body.slice(0,10); // gets first 10 elements
           return data.json() //data.json() is asynchronous task - takes some time to complete
       }).then(function(data){
      var mentorsArray = [];
      for (let key in data){
        // key refers to the unique id in the database;
        // data is the parent object which includes the child objects each one being a different blog post
        data[key].id = key;
        mentorsArray.push(data[key]);
      }
      this.mentors = mentorsArray;
        });
    },

// WORKING JUST FINE:
    computed:{
//    console.log(this.search);
    filteredMentors: function(){
      return this.mentors.filter((mentor) => {
//        console.log(mentor.name.match('a'))
//        console.log(mentor.name.match(this.search))
//        return mentor.name.toUpperCase().match(this.search.toUpperCase());

//        Removing any extra spaces
        cleanSearch = this.search.replace(/\s+/g,' ').trim();
        var lowSearch = cleanSearch.toLowerCase()
        var result = lowSearch.replace(/[^\w\s]|_/g, "").replace(/\s+/g, " ");

        return this.searchProps.some( key =>
        String(mentor[key]).toLowerCase().includes(result) );
//        return keys.some( key =>
//            String(mentor[key]).toUpperCase().includes(upSearch)
            });
        }
    }


// NOT WORKING: TRYING TO HIGHLIGHT THE SEARCH RESULTS
//    computed:{
//        filteredMentors: function(){
//          return this.mentors.filter((mentor) => {
//            var upSearch = this.search.toUpperCase()
//            return this.searchProps.some( key =>
//            String(mentor[key]).toUpperCase().includes(upSearch
////            console.log(String(mentor[key]).toUpperCase().includes(upSearch));
//            );
////            .replace(upSearch, '<span class="highlight">' + query + '</span>')
//                });
//            }
//        }
//


});
