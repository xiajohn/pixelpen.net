import React, { forwardRef } from 'react';
import styles from '../css/Essay.module.css';

const Essay = forwardRef(({content}, ref) => {   
  return (
    <div className={styles.essay} ref={ref}> 
      <h2>Pixel Pen Preview</h2>
      <p dangerouslySetInnerHTML={{__html: content.replace(/\n/g, '<br>')}}></p>
    </div>
  );
})

export default Essay;
