<template>

<div class="panel panel-default"  name="search-planner-group">
  <div class="panel-heading">
    <i class="fa fa-gamepad fa-fw" style="margin-right:5px"></i> 检验结果
    <button class="btn btn-success btn-circle pull-right" v-on:click="train()">
       <i class="fa fa-check fa-fw"></i>
    </button>
  </div>

  <div class="panel-body">
    <table width="100%" class="table table-striped table-bordered table-hover">
      <thead>
        <tr>
         <th>train count</th>
         <th>test count</th>
         <th>success rate</th>
        </tr>
      </thead>
      <tbody>
        <tr class="odd gradeX">
          <td>{{ train_count }}</td>
          <td>{{ test_count }}</td>
          <td>{{ rate }}</td>
        </tr>
      </tbody>
    </table>


    <table width="100%" class="table table-striped table-bordered table-hover">
      <thead>
        <tr>
         <th>game id </th>
         <th>good review count</th>
         <th>bad review count</th>
         <th>rate(svm)</th>
         <th>rate(steam)</th>
        </tr>
      </thead>
      <tbody>
        <tr class="odd gradeX" v-for="game in games">
          <td>{{ game.game_id }}</td>
          <td>{{ game.good }}</td>
          <td>{{ game.bad }}</td>
          <td>{{ game.rate }}</td>
          <td>{{ game.real_rate }}</td>
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
            train_count: "0",
            test_count: "0",
            rate: "0%",
            games : []
        }
    },
    created:function(){
        this.get_result()
    },
    methods: {
        train:function() {
            this.$http.get("/do_train",{
                params: {
                }})
                .then(function (resp) {
                    var data = resp.data
                    this.$data.train_count = data.train_count
                    this.$data.test_count = data.test_count
                    this.$data.rate = data.rate
                },function(){
                    alert("网络不通")
                })
        },

        get_result:function() {
            this.$http.get("/get_result",{
                params: {
                }})
                .then(function (resp) {
                    var data = resp.data
                    this.$data.games = data
                },function(){
                    alert("网络不通")
                })
        }
    }

}


</script>
