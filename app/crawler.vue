<template>

<div class="panel panel-default"  name="search-planner-group">


<!-- create -->
    <div class="modal fade" id="myModalNewGameReview" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title" id="myModalLabel">
                        新建抓取
                    </h4>
                </div>
                <div class="modal-body">
                  <div class="form-group">
                    <input class="form-control" placeholder="game id" v-model="project"></input>
                  </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-dismiss="modal" v-on:click="addProject()">抓取</button>
                </div>
            </div><!-- /.modal-content -->
        </div><!-- /.modal -->
    </div>


  <div class="panel-heading">
    <i class="fa fa-github-square fa-fw" style="margin-right:5px"></i>Search Planner

    <button class="btn btn-success btn-circle pull-right" data-toggle="modal" data-target="#myModalNewGameReview" >
       <i class="fa fa-plus fa-fw"></i>
    </button>
  </div>
  <!-- /.panel-heading -->
  <div v-if="status !=''" class="panel-body" style="min-height:190px" id="all_projects">
    <div class="fill">
        <h2 class="text-center">{{ status }}</h2>
    </div>
  </div>

  <div v-if="status == ''" class="panel-body" id="all_projects">
    <div class="list-group">
         <li class="list-group-item" v-for="repo in repos">
              <h4 class="list-group-item-heading">
                  <i class="fa fa-code-fork fa-fw"></i>
                  {{ repo.name }}
                  <small>{{ repo.desc }}</small>

                   <button class="btn btn-primary btn-circle pull-right" data-toggle="modal" data-target="#myModal" v-on:click="selectRepo(repo.repo)">
                     <i class="fa fa-plus fa-fw"></i>
                   </button>
              </h4>
              <small class="list-group-item-text">
                 {{ repo.repo }}
              </small>
         </li>
    </div>

    <div class="modal fade" id="myModal" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title" id="myModalLabel">
                        创建 {{ repository }} 的分支
                    </h4>
                </div>
                <div class="modal-body">
                    <input class="form-control" placeholder="branch name..." v-model="branch"></input>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-dismiss="modal" v-on:click="createBranch">创建</button>
                </div>
            </div><!-- /.modal-content -->
        </div><!-- /.modal -->
    </div>


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
        repos : [],
        project : "",
        password: "",
        description: "",
        status: "",
        repository: "",
        username: "",
        branch: "" }
    },
    created:function(){
        this.$data.status = "正在载入..."
        this.$data.username = this.user
        this.$http.get("/api/all_projects",{
                  params: {
                      username: this.$data.username
                  }})
                .then(function (resp) {
                    var data = resp_check(resp.data)
                    if(data) {
                        this.$data.repos = data
                        this.$data.status = ""
                    }
                },function(){
                    alert("网络不通")
                })
    },
    methods: {

        selectRepo: function(repo) {
            this.$data.repository = repo
        },

        addProject: function() {

            this.$data.status = "正在创建..."
            this.$http.post("/api/new_project", {
                      username: this.$data.username,
                      password: this.$data.password,
                      description: encodeURI(this.$data.description),
                      project: this.$data.project
                    })
                    .then(function (resp) {
                        var data =resp_check(resp.data)
                        if(data) {
                            this.$data.status = ""
                            window.location.href = "/"
                        }
                    },function(){
                        alert("网络不通")
            })

        },

        createBranch: function() {

            this.$data.status = "正在创建..."
            this.$http.post("/api/new_branch", {
                      username: this.$data.username,
                      repository: this.$data.repository,
                      branch: this.$data.branch
                    })
                    .then(function (resp) {
                        var data =resp_check(resp.data)
                        if(data) {
                            var url = "/editor?username=" + this.$data.username + "&repository=" + this.$data.repository.replace('/', '%2F') + "&branch="  + this.$data.branch
                            window.location.href = url
                            this.$data.status = ""
                        }
                    },function(){
                        alert("网络不通")
            })

        }
    }

}


</script>
