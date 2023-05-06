import React from 'react';
import styles from '../css/Essay.module.css';

function Essay({content}) {
  return (
    <div className={styles.essay}>
      <h2>Pixel Pen Preview</h2>
      <p dangerouslySetInnerHTML={{__html: content.replace(/\n/g, '<br>')}}></p>
    </div>
  );
}

export default Essay;
