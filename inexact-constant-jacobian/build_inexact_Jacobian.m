function Jacobian = build_inexact_Jacobian(Y_bus, num_buses)
    % Initialize the Jacobian sub-matrices J1, J2, J3, and J4 as zero matrices
    J1 = zeros(num_buses - 1);
    J2 = zeros(num_buses - 1);
    J3 = zeros(num_buses - 1);
    J4 = zeros(num_buses - 1);

    % Loop over buses from 2 to N (ignoring the slack bus at index 1)
    for i = 2:num_buses
        Gii = real(Y_bus(i, i)); % Real part (conductance) for bus i
        Bii = imag(Y_bus(i, i)); % Imaginary part (susceptance) for bus i

        % Diagonal Jacobian elements (excluding bus 1)
        J1(i-1, i-1) = sum(imag(Y_bus(i, :))) - Bii;
        J2(i-1, i-1) = 2 * Gii + sum(real(Y_bus(i, :))) - Gii;
        J3(i-1, i-1) = sum(real(Y_bus(i, :))) - Gii;
        J4(i-1, i-1) = -2 * Bii - sum(imag(Y_bus(i, :))) + Bii;

        % Off-diagonal Jacobian elements
        for j = 2:num_buses  % Excluding bus 1 (slack bus)
            if i ~= j
                Gij = real(Y_bus(i, j)); % Real part (off-diagonal)
                Bij = imag(Y_bus(i, j)); % Imaginary part (off-diagonal)

                J1(i-1, j-1) = -Bij;  % Off-diagonal elements
                J2(i-1, j-1) = Gij;
                J3(i-1, j-1) = -Gij;
                J4(i-1, j-1) = -Bij;
            end
        end
    end

    % Combine submatrices to form the complete Jacobian
    Jacobian = [J1, J2; J3, J4];
end
