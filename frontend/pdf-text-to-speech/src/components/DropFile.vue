
<template>
  <div class="container">
    <div>
      <h2>Single File</h2>
      <hr/>
      <label>File
        <input type="file" @change="handleFileUpload( $event )"/>
      </label>
      <br>
      <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
</template>


<script>

import axios from 'axios'

  export default {
    data(){
        return {
            file: ''
        }
    },
    methods: {
      handleFileUpload( event ){
        this.file = event.target.files[0];
    },
    submitFile(){
        let formData = new FormData();
        formData.append('file', this.file);
        console.log(this.file)
        if(this.file['type']==='application/pdf'){
            
            axios.post( 'http://localhost:8003/pdf',
                formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
                , //
                responseType: "blob",
                config: {
                    headers: {
                    'Accept': 'audio/mpeg'
                }
    }
              }
              , {responseType: 'blob'}).then(function (response) {
                console.log(response)
        const url = window.URL.createObjectURL(new Blob([response.data],
            { type: 'audio/mpeg' }));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download',
            response.headers["content-disposition"].split("filename=")[1]);
        document.body.appendChild(link);
        link.click();
    }
)
        .catch(function(){
          console.log('FAILURE!!');
        });
        }
    
      },
    }
  }
</script>