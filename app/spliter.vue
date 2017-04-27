<template>

<div class="panel panel-default"  name="search-planner-group">


  <div class="panel-heading">
    <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 分词
    <button class="btn btn-success btn-circle pull-right" v-on:click="spliter()">
       <i class="fa fa-check fa-fw"></i>
    </button>
  </div>

  <!-- /.panel-heading -->

  <div v-if="status !=''" class="panel-body" style="min-height:190px" id="all_projects">
    <div class="fill">
        <h2 class="text-center">{{ status }}</h2>
    </div>
  </div>
  <div v-if="status == ''" class="panel-body" id="all_projects">
    <table width="100%" class="table table-striped table-bordered table-hover" id="dataTables-example2">
      <thead>
        <tr>
         <th>ID</th>
         <th>Game</th>
         <th>Words</th>
        </tr>
      </thead>
      <tbody>
        <tr class="odd gradeX" v-for="word in words">
          <td>{{ word.review_id }}</td>
          <td>{{ word.game_id }}</td>
          <td>
               <ul>
                 <li v-for="w in word.words"> {{ w[0] }}  {{ w[1] }}</li>
               </ul>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

</div>

</template>

<script>

export default{
    props: {
        user: String
    },
    data: function() {
        return {
            words: [],
            game_id : "",
            status : "",
            review_count : 0,
            pages: [],
        }
    },
    created:function(){
        this.show_words()
        setTimeout(() => {
            $('#dataTables-example2').DataTable({
            });
        }, 100)
    },
    methods: {

        show_words:function() {
            this.$http.get("/words",{
                params: {
                }})
                .then(function (resp) {
                    var data = resp.data
                    if(data) {
                        this.$data.status = ""
                        this.$data.words = data
                    }
                },function(){
                    alert("网络不通")
                })

        },

        spliter:function() {
            this.$data.status = "正在分词提取..."
            this.$http.get("/split",{
                params: {
                }})
                .then(function (resp) {
                    this.show_words()
                },function(){
                    alert("网络不通")
                })
        }

    }

}


</script>
