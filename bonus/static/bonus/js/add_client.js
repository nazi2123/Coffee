document.getElementById('phone').addEventListener('input', function (e) {
    let digits = e.target.value.replace(/\D/g, '');

    if (digits && digits[0] !== '7') {
        digits = '7' + digits;
    }

    if (digits.startsWith('7')) {
        digits = digits.slice(1);
    }

    const part1 = digits.substring(0, 3);
    const part2 = digits.substring(3, 6);
    const part3 = digits.substring(6, 8);
    const part4 = digits.substring(8, 10);

    let formatted = '+7';
    if (part1) {
        formatted += ' (' + part1;
        if (part1.length === 3) {
            formatted += ')';
        }
    }
    if (part2) {
        formatted += ' ' + part2;
    }
    if (part3) {
        formatted += '-' + part3;
    }
    if (part4) {
        formatted += '-' + part4;
    }

    e.target.value = formatted;
});