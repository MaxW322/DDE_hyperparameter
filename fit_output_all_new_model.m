function fit_y = fit_output_all(value)
    value = cell2mat(value);
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
    b = (omega-phi*r*x(6)/K);
    d = (mu+(1-phi)*r*x(6)/K)
    u1 = ?;
    u3 = ?;
    ddefun = @(t,x,Z)[
            b*x(6)-(beta_bd*(Z(3,1)+Z(4,1))/Z(6,1))*x(1) - d*x(1);
            (beta_bd*(Z(3,1)+Z(4,1))/Z(6,1))*x(1)- ((Z(3,1)*i_I+Z(4,1)*i_Q)/(Z(3,1)+Z(4,1)))*x(2) - u1*x(2) - d*x(2);
            u1*x(2) -




            b*x(6)-d*x(6);

%            (omega-phi*r*x(6)/K)*x(6)-(beta_bd*(Z(3,1)+Z(4,1))/Z(6,1))*x(1)-(mu+(1-phi)*r*x(6)/K)*x(1);
%            (beta_bd*(Z(3,1)+Z(4,1))/Z(6,1))*x(1) - (mu+(1-phi)*r*x(6)/K)*x(2) - (Z(3,1)*i_I+Z(4,1)*i_Q)*x(2)/(Z(3,1)+Z(4,1));
%            (Z(3,1)*i_I+Z(4,1)*i_Q)*x(2)/(Z(3,1)+Z(4,1)) - beta_ir*x(3) - beta_iq*x(3) - (mu+(1-phi)*r*x(6)/K)*x(3);
%            beta_iq*x(3) - beta_qr*x(4) - (mu+(1-phi)*r*x(6)/K)*x(4) - gamma_2*x(4);
%            beta_qr*x(4) + beta_ir*x(3) - (mu+(1-phi)*r*x(6)/K)*x(5);
%            (omega-phi*r*x(6)/K)*x(6)-(mu+(1-phi)*r*x(6)/K)*x(6);
        ];
    
    options = ddeset('RelTol',1,'AbsTol',10);
    sol = dde23(ddefun,[1 1 1 1 1 1],[1154633644,288658411,1218,776,34,1443497378],[1,135]);
    tint = linspace(1,135,135);
    l = length(sol.y(4,:));

    x = linspace(1,l,l);

%    if l < 135
%        solv = sol.y;
%        sols = pchip(x,solv,tint);
%    end
%
%    if l == 135
%       sols = sol.y;
%    end
%
%    if l > 135
%        sols = 1:135;
%        n = idivide(int32(l),int32(135),'round');
%        for j = 1:6
%            i = 1;
%            while i < 135
%                sols(j,i) = sol.y(j,i);
%                i = i+n;
%            end
%        end
%        if length(sols(1,:)) < 135
%            sols(:,135) = sol.y(:,l);
%        end
%    end
    if l == 135
       sols = sol.y;
    else
        solv = sol.y;
        sols = pchip(x,solv,tint);
    end

    fit_y = round(sols);


end