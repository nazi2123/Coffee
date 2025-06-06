
// Открытие/закрытие модальных окон
const depositBtn = document.getElementById('deposit-btn');
const withdrawBtn = document.getElementById('withdraw-btn');
const depositModal = document.getElementById('deposit-modal');
const withdrawModal = document.getElementById('withdraw-modal');
const closeDeposit = document.getElementById('close-deposit');
const closeWithdraw = document.getElementById('close-withdraw');


if (depositBtn) {
    depositBtn.addEventListener('click', () => {
        depositModal.style.display = 'flex';
    });
}
if (withdrawBtn) {
    withdrawBtn.addEventListener('click', () => {
        withdrawModal.style.display = 'flex';
    });
}
closeDeposit.addEventListener('click', () => {
    depositModal.style.display = 'none';
});
closeWithdraw.addEventListener('click', () => {
    withdrawModal.style.display = 'none';
});

// Расчет 5% бонуса при вводе суммы заказа
const orderSumDeposit = document.getElementById('order_sum_deposit');
const calculatedBonus = document.getElementById('calculated-bonus');
if (orderSumDeposit) {
    orderSumDeposit.addEventListener('input', () => {
        let sum = parseFloat(orderSumDeposit.value) || 0;
        let bonus = Math.floor(sum * 0.05);
        calculatedBonus.textContent = bonus;
    });
}

// Расчет списания баллов и итоговой суммы к оплате
const orderSumWithdraw = document.getElementById('order_sum_withdraw');
const updatedPrice = document.getElementById('updated-price');
const pointsToUse = document.getElementById('points-to-use');

if (orderSumWithdraw) {
    orderSumWithdraw.addEventListener('input', () => {
        let sum = parseFloat(orderSumWithdraw.value) || 0;
        let toUse = Math.min(currentBalance, Math.floor(sum));
        let finalCost = sum - toUse;
        if (toUse >= sum) {
            finalCost = 1; // если баллов больше или равно цене, минимальная цена — 1 руб.
            toUse = sum - 1; // использовать все баллы, кроме 1 рубля
        }
        updatedPrice.textContent = finalCost < 1 ? 1 : finalCost;
        pointsToUse.textContent = toUse;
    });
}