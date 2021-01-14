const downloadSample = sample_id => {
    fetch('sample/' + sample_id, {
    method: 'GET',
    })
    .then(res => res.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a')
      link.href = url
      link.download = `${sample_id}.webm`
      link.click()
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