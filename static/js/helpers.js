const downloadSample = sample_id => {
    console.log(sample_id)
    fetch('sample/' + sample_id, {
    method: 'GET',
    })
    .then(res => res.blob())
    .then(blob => {
      const file = window.URL.createObjectURL(blob);
      window.location.assign(file);
    });
}

const deleteSample = sample_id => {
    fetch('sample/' + sample_id, {
    method: 'DELETE',
    })
    .then(res => res.json())
    .then(res => {
      location.reload();
      return false
    })
}