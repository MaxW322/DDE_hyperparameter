function error = para_all_divide(value)
    warning('off');
    value = cell2mat(value);
    actual = readmatrix('./data/currentconfirmed.csv');
    pos = value(8);
    if (pos < 3)
        start = 1;
        ending = 5;
    elseif ((135-pos) < 3)
        start = 130;
        ending = 135;
    else
        start = pos - 2;
        ending = pos + 2;
    end

    actual_used = actual(start:ending)';

    i_I = value(1);
    i_Q =value(2);
    beta_iq =value(3);
    beta_ir =value(4);
    beta_qr =value(5);
    gamma_2 =value(6);
    beta_bd =value(7);
    phi = 0.014 ;
    omega = 0.00020602739;
    mu = 0.0001967123;
    K = 1500000000;
    r = omega - mu;
    ddefun = @(t,x,Z)[
            (omega-phi*r*x(6)/K)*x(6)-(beta_bd*(Z(3,1)+Z(4,1))/Z(6,1))*x(1)-(mu+(1-phi)*r*x(6)/K)*x(1);
            (beta_bd*(Z(3,1)+Z(4,1))/Z(6,1))*x(1) - (mu+(1-phi)*r*x(6)/K)*x(2) - (Z(3,1)*i_I+Z(4,1)*i_Q)*x(2)/(Z(3,1)+Z(4,1));
            (Z(3,1)*i_I+Z(4,1)*i_Q)*x(2)/(Z(3,1)+Z(4,1)) - beta_ir*x(3) - beta_iq*x(3) - (mu+(1-phi)*r*x(6)/K)*x(3);
            beta_iq*x(3) - beta_qr*x(4) - (mu+(1-phi)*r*x(6)/K)*x(4) - gamma_2*x(4);
            beta_qr*x(4) + beta_ir*x(3) - (mu+(1-phi)*r*x(6)/K)*x(5);
            (omega-phi*r*x(6)/K)*x(6)-(mu+(1-phi)*r*x(6)/K)*x(6);
        ];
    
    options = ddeset('RelTol',1,'AbsTol',10);
    sol = dde23(ddefun,[1 1 1 1 1 1],[1154633644,288658411,1218,776,34,1443497378],[1,135]);
    tint = linspace(1,135,135);
    l = length(sol.y(4,:));

    x = linspace(1,l,l);

%    if l < 135
%        solv = sol.y(4,:);
%        sols = pchip(x,solv,tint);
%    end
%
%    if l == 135
%       sols = sol.y(4,:);
%    end
%
%    if l > 135
%        sols = 1:135;
%        n = idivide(int32(l),int32(135),'round');
%        i = 1;
%        while i < 135
%            sols(i) = sol.y(4,i);
%            i = i+n;
%        end
%        if length(sols) < 135
%            sols(135) = sol.y(4,l);
%        end
%    end
    if l == 135
       sols = sol.y(4,:);
    else
        solv = sol.y(4,:);
        sols = pchip(x,solv,tint);
    end
    sols = round(sols);
    error = sqrt(mse(sols(start:ending),actual_used));
%    error = sqrt(mse(sols(pos),actual));

end