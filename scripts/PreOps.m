

%PROBLEM 2

%load data
data = readtable('PreOpsDataV2.xlsx')

%X = table2array(readtable('CSdata.xlsx'))
%Separate data
%Y = data(:,3);
%X1X2 = data(:,1:2);
%Exam1 = data(:,1);
%Exam2 = data(:,2);


%Decision Tree

%Set decision tree
Model = fitctree(data,'Hardware~DesiredTemperature+X+Y+Z');

%Divide dataset into training set and test set
cv = cvpartition(Model.NumObservations,'HoldOut',0.2);

%Use training set to train model
cross_validated_model = crossval(Model,'cvpartition',cv);

%Use test set to test the decision tree
Predictions = predict(cross_validated_model.Trained{1},data(test(cv),1:end-1));

%Visualize tree
view(cross_validated_model.Trained{1},'mode','graph')

A = table2array(data(test(cv),8))
%D = sort(A)
Predictions
Final = data(test(cv), 1:end-1);
Final(:,8) = Predictions;
Out = sortrows(Final,8)

G = findgroups(Final{:,8}) %doesn't find groups of sorted array
%for i == g... 
%Tc = splitapply( @(varargin) varargin, Final, G)

strcmp(A,Predictions);

%Compare and print out accuracy of the test set 
fprintf('Prediction Accuracy Via Decision Tree on The Test Set: %4.2f\n',...
    sum(strcmp(A,Predictions))/length(A)*100);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Visualize the testing data
