
function deepCopy(src) {
    return JSON.parse(JSON.stringify(src));
}


function fft_ifft(re, im, ifft=false) {
    let xRe = deepCopy(re);
    let xIm = deepCopy(im);

    if(ifft) {
        xIm = xIm.map(v => -1 * v);
    }

    let n = re.length;
    let nv2 = n / 2;
    const PI = Math.PI;
    let tRe,tIm;

    let j = 0;
    for(let i = 0; i<n-1; i++) {
        if(j < i) {
            tRe = xRe[j];
            tIm = xIm[j];
            xRe[j] = xRe[i];
            xIm[j] = xIm[i];
            xRe[i] = tRe;
            xIm[i] = tIm;
        }

        let k = nv2;
        while(j>=k) {
            j -=k;
            k /= 2;
        }
        j += k
    }

    for (let i = 0; i <= Math.log2(n); i++) {
        let ie = 1 << i;
        let ie1 = ie >> 1;

        let uRe = 1.0, uIm = 0.0;
        let wRe = Math.cos(PI/ie1), wIm = -1 * Math.sin(PI/ie1);

        for(let j = 0; j < ie1; j++) {
            for(let k = j; k < n; k+=ie) {
                let ip = k + ie1;
                tRe = xRe[ip] * uRe - xIm[ip] * uIm;
                tIm = xRe[ip] * uIm + xIm[ip] * uRe;
                xRe[ip] = xRe[k] - tRe;
                xIm[ip] = xIm[k] - tIm;
                xRe[k] += tRe;
                xIm[k] += tIm;
            }
            let vRe = uRe * wRe - uIm * wIm;
            let vIm = uRe * wIm + uIm * wRe;
            uRe = vRe;
            uIm = vIm;
        }
    }

    if(ifft) {
        for(let i = 0; i<n; i++) {
            xRe[i] /= n;
            xIm[i] /= -n;
        }
    }
    return {re: xRe, im: xIm};
}
